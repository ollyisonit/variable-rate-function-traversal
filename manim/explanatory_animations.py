from manim import *

AXIS_LENGTH = 8 * PI
TIME_LENGTH = 10


def omega_func(t):
    a = 3 * PI
    b = 5 * PI
    f1 = 1
    f2 = 5
    if (t < a):
        return f1
    if t > b:
        return f2
    return ((f2 - f1) / (b - a)) * (t - a) + f1


def bad_solution(t):
    return np.sin(omega_func(t) * t)


def good_solution(t):
    # DONT FORGET TO FIX FOR FINAL EXPORT
    d = 0.05
    samples = [omega_func(x * d) for x in range(0, int(t / d))]
    return np.sin(np.trapz(samples, dx=d))


class SimpleSine(Scene):

    def construct(self):
        tracker = ValueTracker(0.01)

        sine_axes = Axes(x_range=[0, AXIS_LENGTH, 1],
                         x_length=5,
                         y_range=[-2, 2, 1],
                         y_length=3,
                         axis_config={
                             'include_ticks': False,
                             'include_tip': False
                         }).shift(LEFT * 3)

        sine_graph = always_redraw(lambda: sine_axes.plot(
            lambda x: np.sin(x), x_range=[0, tracker.get_value()]).set_color(
                YELLOW))
        sine_dot = always_redraw(lambda: Dot(fill_color=BLUE).scale(1).move_to(
            sine_graph.get_end()))

        dot_axes = Axes(x_range=[-1, 1, 1],
                        x_length=3,
                        y_range=[-2, 2, 1],
                        y_length=3).next_to(sine_axes, RIGHT,
                                            buff=0.1).set_opacity(0)
        dot = always_redraw(lambda: Dot(fill_color=BLUE).scale(5).move_to(
            dot_axes.coords_to_point(0, np.sin(tracker.get_value()))))

        graph_and_dot = Group(sine_axes, sine_graph, sine_dot, dot_axes, dot)

        graph_and_dot.move_to(ORIGIN)

        title = MathTex(r"f(t)=sin(\omega * t)").next_to(graph_and_dot,
                                                         DOWN,
                                                         buff=0.2)

        self.add(graph_and_dot, title)
        self.play(tracker.animate.set_value(AXIS_LENGTH),
                  run_time=TIME_LENGTH,
                  rate_func=linear)


class ExpandContract(Scene):

    def construct(self):
        tracker = ValueTracker(0.25)
        sine_axes = Axes(x_range=[0, AXIS_LENGTH * 2, 1],
                         x_length=5,
                         y_range=[-2, 2, 1],
                         y_length=3,
                         axis_config={
                             'include_ticks': False,
                             'include_tip': False
                         }).shift(LEFT * 3)
        sine_graph = always_redraw(lambda: sine_axes.plot(
            lambda x: np.sin(tracker.get_value() * x),
            x_range=[0, (4 * PI) / tracker.get_value()]).set_color(YELLOW))

        omega_label = always_redraw(
            lambda: MathTex(f"\\omega = ").next_to(sine_axes, DOWN, buff=0.2))

        num = DecimalNumber(0)
        num.add_updater(lambda m: m.set_value(tracker.get_value()))
        num.next_to(omega_label, RIGHT)

        label_grp = Group(omega_label, num)

        group = Group(sine_axes, sine_graph, label_grp).move_to(ORIGIN, ORIGIN)

        self.add(group)
        self.play(tracker.animate.set_value(2), run_time=2, rate_func=linear)
        self.wait()
        self.play(tracker.animate.set_value(0.25),
                  run_time=2,
                  rate_func=linear)
        self.wait()


class MysteryFunction(Scene):

    def construct(self):
        tracker = ValueTracker(0.01)

        sine_axes = Axes(x_range=[0, AXIS_LENGTH, 1],
                         x_length=4,
                         y_range=[-2, 2, 1],
                         y_length=3,
                         axis_config={
                             'include_ticks': False,
                             'include_tip': False
                         }).shift(LEFT * 3)

        sine_graph = always_redraw(lambda: sine_axes.plot(
            lambda x: good_solution(x), x_range=[0, tracker.get_value()]).
                                   set_color(YELLOW))
        sine_dot = always_redraw(lambda: Dot(fill_color=BLUE).scale(1).move_to(
            sine_graph.get_end()))

        dot_axes = Axes(x_range=[-1, 1, 1],
                        x_length=2,
                        y_range=[-2, 2, 1],
                        y_length=3).next_to(sine_axes, RIGHT,
                                            buff=0.1).set_opacity(0)
        dot = always_redraw(lambda: Dot(fill_color=BLUE).scale(5).move_to(
            dot_axes.coords_to_point(0, good_solution(tracker.get_value()))))

        graph_and_dot = Group(sine_axes, sine_graph, sine_dot, dot_axes, dot)

        title = MathTex(r"f(t) =\text{?}").next_to(sine_axes, DOWN, buff=0.2)

        oscillating_group = Group(graph_and_dot, title)

        omega_axes = Axes(x_range=[0, AXIS_LENGTH, 1],
                          x_length=4,
                          y_range=[-7, 7, 1],
                          y_length=3,
                          axis_config={
                              'include_ticks': False,
                              'include_tip': False
                          }).shift(LEFT * 3)

        omega_graph = always_redraw(lambda: omega_axes.plot(
            lambda x: omega_func(x), x_range=[0, tracker.get_value()]).
                                    set_color(YELLOW))
        omega_dot = always_redraw(lambda: Dot(fill_color=BLUE).scale(1).
                                  move_to(omega_graph.get_end()))

        omega_graph_and_dot = Group(omega_axes, omega_graph, omega_dot)
        omega_title = MathTex("\\omega (t)").next_to(omega_axes,
                                                     DOWN,
                                                     buff=0.2)

        omega_group = Group(omega_graph_and_dot, omega_title)

        omega_group.next_to(oscillating_group, LEFT, buff=0.5)

        full_group = Group(omega_group, oscillating_group)

        full_group.move_to(ORIGIN, ORIGIN)

        self.add(full_group)
        self.play(tracker.animate.set_value(AXIS_LENGTH),
                  run_time=TIME_LENGTH,
                  rate_func=linear)
