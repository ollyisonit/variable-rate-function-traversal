from manim import *
from math import sin


class Scene1(Scene):

    def construct(self):
        AXIS_LENGTH = 30
        TIME_LENGTH = 10

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
            lambda x: np.sin(x), x_range=[0, tracker.get_value()]))
        sine_dot = always_redraw(lambda: Dot(fill_color=GOLD).scale(0.5).
                                 move_to(sine_graph.get_end()))

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
        self.play(tracker.animate.set_value(AXIS_LENGTH * 0.95),
                  run_time=TIME_LENGTH,
                  rate_func=linear)
