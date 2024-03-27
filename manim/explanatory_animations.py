from typing import Sequence
from manim import *

AXIS_LENGTH = 8 * PI
TIME_LENGTH = 10
RIEMANN_STEP = 0.01


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


def good_solution_integrate(t):
    # DONT FORGET TO MAKE SMALLER FOR FINAL EXPORT
    d = RIEMANN_STEP
    samples = [omega_func(x * d) for x in range(0, int(t / d))]
    return np.trapz(samples, dx=d)


def good_solution(t):
    return np.sin(good_solution_integrate(t))


def build_animated_graph(
        label: Mobject,
        function: Callable[[float], float],
        tracker: ValueTracker,
        x_range: Sequence[float] = [-5, 5, 1],
        x_length: float = 5,
        y_range: Sequence[float] = [-5, 5, 1],
        y_length: float = 5,
        axis_config={
            'include_ticks': False,
            'include_tip': False
        }) -> Mobject:
    axes = Axes(x_range=x_range,
                x_length=x_length,
                y_range=y_range,
                y_length=y_length,
                axis_config=axis_config)

    graph = always_redraw(lambda: axes.plot(
        function, x_range=[0, tracker.get_value()]).set_color(YELLOW))
    dot = always_redraw(
        lambda: Dot(fill_color=BLUE).scale(1).move_to(graph.get_end()))
    graph_group = Group(axes, graph, dot)
    if label != None:
        title = label.next_to(axes, DOWN, buff=0.2)
        graph_group = Group(graph_group, title)
    return graph_group


def build_bouncing_ball(function: Callable[[float], float],
                        tracker: ValueTracker,
                        x_range=[-1, 1, 1],
                        x_length=10 * DEFAULT_DOT_RADIUS,
                        y_range=[-2, 2, 1],
                        y_length=3) -> Mobject:
    dot_axes = Axes(x_range=x_range,
                    x_length=x_length,
                    y_range=y_range,
                    y_length=y_length).set_opacity(0)
    dot = always_redraw(
        lambda: Dot(fill_color=BLUE, radius=x_length / 2).move_to(
            dot_axes.coords_to_point(0, function(tracker.get_value()))))
    return Group(dot_axes, dot)


def build_side_by_side(functions: tuple[Mobject, Callable[[float], float]],
                       tracker: ValueTracker) -> Mobject:
    tracker = ValueTracker(0.01)

    x_width: float = 8 / len(functions)
    graphs: List[Mobject] = []

    for (title, function) in functions:
        f_graph = build_animated_graph(title,
                                       function,
                                       tracker,
                                       x_range=[0, AXIS_LENGTH, 1],
                                       x_length=x_width,
                                       y_range=[-2, 2, 1],
                                       y_length=3,
                                       axis_config={
                                           'include_ticks': False,
                                           'include_tip': False
                                       })
        graphs.append(f_graph)

    for i in range(1, len(graphs)):
        graphs[i].next_to(graphs[i - 1], RIGHT, buff=0.2)

    graphs_group = Group(graphs)

    ball = build_bouncing_ball(function,
                               tracker,
                               x_length=10 * DEFAULT_DOT_RADIUS).next_to(
                                   graphs_group, RIGHT, buff=1)

    full_group = Group(graphs_group, ball)

    full_group.move_to(ORIGIN, ORIGIN)

    return full_group


class SimpleSine(Scene):

    def construct(self):
        tracker = ValueTracker(0.01)

        sine_graph = build_animated_graph(
            None,
            lambda x: np.sin(x),
            tracker,
            x_range=[0, AXIS_LENGTH, 1],
            x_length=5,
            y_range=[-2, 2, 1],
            y_length=3,
        )

        dot = build_bouncing_ball(lambda x: np.sin(x),
                                  tracker).next_to(sine_graph, RIGHT, buff=1)

        graph_and_dot = Group(sine_graph, dot)

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

        f_graph = build_animated_graph(MathTex(r"f(t) =\text{?}"),
                                       good_solution,
                                       tracker,
                                       x_range=[0, AXIS_LENGTH, 1],
                                       x_length=4,
                                       y_range=[-2, 2, 1],
                                       y_length=3,
                                       axis_config={
                                           'include_ticks': False,
                                           'include_tip': False
                                       })

        ball = build_bouncing_ball(good_solution,
                                   tracker,
                                   x_length=10 * DEFAULT_DOT_RADIUS).next_to(
                                       f_graph, RIGHT, buff=1)

        oscillating_group = Group(f_graph, ball)

        omega_group = build_animated_graph(MathTex("\\omega (t)"),
                                           omega_func,
                                           tracker,
                                           x_range=[0, AXIS_LENGTH, 1],
                                           x_length=4,
                                           y_range=[-7, 7, 1],
                                           y_length=3,
                                           axis_config={
                                               'include_ticks': False,
                                               'include_tip': False
                                           }).shift(LEFT * 3)

        oscillating_group.next_to(omega_group, RIGHT, buff=0.5)

        full_group = Group(omega_group, oscillating_group)

        full_group.move_to(ORIGIN, ORIGIN)

        self.add(full_group)
        self.play(tracker.animate.set_value(AXIS_LENGTH),
                  run_time=TIME_LENGTH,
                  rate_func=linear)


class BadFunction(Scene):

    def construct(self):
        tracker = ValueTracker(0.01)

        bad_graph = build_animated_graph(
            MathTex(r"f(t) = sin(\omega(t) * t)").scale(0.8),
            bad_solution,
            tracker,
            x_range=[0, AXIS_LENGTH, 1],
            x_length=4,
            y_range=[-2, 2, 1],
            y_length=3,
            axis_config={
                'include_ticks': False,
                'include_tip': False
            })

        ball = build_bouncing_ball(bad_solution,
                                   tracker,
                                   x_length=10 * DEFAULT_DOT_RADIUS).next_to(
                                       bad_graph, RIGHT, buff=1)

        graph_and_dot = Group(bad_graph, ball)

        omega_graph = build_animated_graph(MathTex("\\omega (t)").scale(0.9),
                                           omega_func,
                                           tracker,
                                           x_range=[0, AXIS_LENGTH, 1],
                                           x_length=4,
                                           y_range=[-7, 7, 1],
                                           y_length=3,
                                           axis_config={
                                               'include_ticks': False,
                                               'include_tip': False
                                           }).next_to(graph_and_dot,
                                                      LEFT,
                                                      buff=0.5)

        full_group = Group(omega_graph, graph_and_dot)

        full_group.move_to(ORIGIN, ORIGIN)

        self.add(full_group)
        self.play(tracker.animate.set_value(AXIS_LENGTH),
                  run_time=TIME_LENGTH,
                  rate_func=linear)


class BadFunctionExplanation(Scene):

    def construct(self):
        tracker = ValueTracker(0.01)

        omega_graph = build_animated_graph(MathTex("\\omega (t)").scale(0.9),
                                           omega_func,
                                           tracker,
                                           x_range=[0, AXIS_LENGTH, 1],
                                           x_length=4,
                                           y_range=[-7, 7, 1],
                                           y_length=3,
                                           axis_config={
                                               'include_ticks': False,
                                               'include_tip': False
                                           })

        omega_graph_exp = build_animated_graph(
            MathTex("\\omega (t) * t").scale(0.9),
            lambda x: x * omega_func(x),
            tracker,
            x_range=[0, AXIS_LENGTH, 1],
            x_length=4,
            y_range=[-7, AXIS_LENGTH * omega_func(AXIS_LENGTH) + 10, 1],
            y_length=3,
            axis_config={
                'include_ticks': False,
                'include_tip': False
            }).next_to(omega_graph, RIGHT, buff=0.5)

        bad_graph = build_animated_graph(
            MathTex(r"f(t) = sin(\omega(t) * t)").scale(0.8),
            bad_solution,
            tracker,
            x_range=[0, AXIS_LENGTH, 1],
            x_length=4,
            y_range=[-2, 2, 1],
            y_length=3,
            axis_config={
                'include_ticks': False,
                'include_tip': False
            }).next_to(omega_graph_exp, RIGHT, buff=0.5)

        full_group = Group(omega_graph, omega_graph_exp, bad_graph)

        full_group.move_to(ORIGIN, ORIGIN)

        self.add(full_group)
        self.play(tracker.animate.set_value(AXIS_LENGTH),
                  run_time=TIME_LENGTH,
                  rate_func=linear)


class GoodFunctionExplanation(Scene):

    def construct(self):
        tracker = ValueTracker(0.01)

        omega_graph = build_animated_graph(MathTex("\\omega (t)").scale(0.9),
                                           omega_func,
                                           tracker,
                                           x_range=[0, AXIS_LENGTH, 1],
                                           x_length=4,
                                           y_range=[-7, 7, 1],
                                           y_length=3,
                                           axis_config={
                                               'include_ticks': False,
                                               'include_tip': False
                                           })

        omega_graph_exp = build_animated_graph(
            MathTex("g(t)").scale(0.9),
            good_solution_integrate,
            tracker,
            x_range=[0, AXIS_LENGTH, 1],
            x_length=4,
            y_range=[-7, AXIS_LENGTH * omega_func(AXIS_LENGTH) + 10, 1],
            y_length=3,
            axis_config={
                'include_ticks': False,
                'include_tip': False
            }).next_to(omega_graph, RIGHT, buff=0.5)

        bad_graph = build_animated_graph(
            MathTex(r"f(t) = sin(g(t))").scale(0.8),
            good_solution,
            tracker,
            x_range=[0, AXIS_LENGTH, 1],
            x_length=4,
            y_range=[-2, 2, 1],
            y_length=3,
            axis_config={
                'include_ticks': False,
                'include_tip': False
            }).next_to(omega_graph_exp, RIGHT, buff=0.5)

        full_group = Group(omega_graph, omega_graph_exp, bad_graph)

        full_group.move_to(ORIGIN, ORIGIN)

        self.add(full_group)
        self.play(tracker.animate.set_value(AXIS_LENGTH),
                  run_time=TIME_LENGTH,
                  rate_func=linear)


class SpeedVariation(Scene):

    def construct(self):
        tracker = ValueTracker(0.01)

        omega_graph = build_animated_graph(MathTex("\\omega (t)").scale(0.9),
                                           omega_func,
                                           tracker,
                                           x_range=[0, AXIS_LENGTH, 1],
                                           x_length=3,
                                           y_range=[-7, 7, 1],
                                           y_length=3,
                                           axis_config={
                                               'include_ticks': False,
                                               'include_tip': False
                                           })

        oscillate_axes = Axes(
            x_range=[0, good_solution_integrate(AXIS_LENGTH), 1],
            x_length=6,
            y_range=[-2, 2, 1],
            y_length=3,
            axis_config={
                'include_ticks': False,
                'include_tip': False
            })

        oscillate_graph = always_redraw(
            lambda: oscillate_axes.plot_parametric_curve(
                lambda t: [good_solution_integrate(t),
                           good_solution(t)],
                t_range=[0, tracker.get_value()]).set_color(YELLOW))
        oscillate_dot = always_redraw(lambda: Dot(fill_color=BLUE).scale(1).
                                      move_to(oscillate_graph.get_end()))
        oscillate_arrow = always_redraw(
            lambda: oscillate_axes.plot_parametric_curve(
                lambda t: [good_solution_integrate(t), 1.75],
                t_range=[0, tracker.get_value()]).set_color(GREEN))
        oscillate_arrowhead = always_redraw(
            lambda: ArrowTriangleFilledTip(fill_color=GREEN).scale(0.7).rotate(
                PI).move_to(oscillate_arrow.get_end()))
        oscillate_arrowhead_title = always_redraw(
            lambda: MathTex("\\omega (t)").scale(0.75).set_color(GREEN).
            next_to(oscillate_arrowhead, np.array((0.4, 0.65, 0)), buff=0.1))
        oscillate_title = MathTex("f(t)").next_to(oscillate_axes,
                                                  DOWN,
                                                  buff=0.2)
        oscillate_group = Group(oscillate_axes, oscillate_arrow,
                                oscillate_graph, oscillate_dot,
                                oscillate_title, oscillate_arrowhead,
                                oscillate_arrowhead_title)

        oscillate_group.next_to(omega_graph, RIGHT, buff=0.5)

        bouncing_ball = build_bouncing_ball(
            good_solution, tracker,
            x_length=10 * DEFAULT_DOT_RADIUS).next_to(oscillate_axes,
                                                      RIGHT,
                                                      buff=1)

        full_group = Group(oscillate_group, omega_graph, bouncing_ball)

        full_group.move_to(ORIGIN, ORIGIN)

        self.add(full_group)
        self.play(tracker.animate.set_value(AXIS_LENGTH),
                  run_time=TIME_LENGTH,
                  rate_func=linear)
