import gc
from manim import *


class SubShapeTest(Scene):
    def construct(self):
        group = Group()
        colors = color_gradient([PURE_GREEN, PURE_BLUE, PURE_RED, YELLOW_C], 12)
        square = Square()
        square.set_stroke(colors[0], width=3)

        self.play(
            Create(square),
        )
        self.play(
            square.animate.scale(2)
        )

        group.add(square, square.copy())
        for i in range(16):
            tmp = group.submobjects[-1].copy()
            self.play(
                tmp.animate.scale(.9).rotate(-1.5 * DEGREES).set_color(color=colors[i % 12]), run_time=0.06
            )
            group.add(tmp)

        # REVERSE ROTATION
        group_list = group.submobjects
        l = len(group_list)

        indices = np.arange(l - 1, 1, -1)
        sub_group = Group()

        for i in indices:
            sub_group.add(group_list[i])
            self.play(
                sub_group.animate
                .rotate(1.5 * DEGREES)
                , run_time=0.06
            )

        ## Fade out group!
        for i in indices:
            obj = group_list[i]
            self.play(
                FadeOut(obj),
                run_time=0.06
            )

        group.remove(group.submobjects)
        sub_group.remove(sub_group.submobjects)
        gc.collect()

class FractalTest(Scene):
    global_group = Group()

    def construct(self):
        fract = Triangle().scale(5).set_stroke(color=BLUE_A, width=2)
        self.play(
            Create(fract),
            run_time=1
        )
        fract = self.fractal(fract, 2, 0)

        self.play(fract.animate.scale(.5))

        #fract2 = fract.copy()
        #self.play(fract.animate.shift(RIGHT*2.1))
        #self.play(fract2.animate.shift(LEFT*2.1))

        self.wait(1)

    # This works really well but we end up saving the old fractal objects [ remove(tri) tries to fix this, needs profiling]
    def fractal(self, fractal, depth, count):
        f0 = fractal.copy().scale(np.true_divide(1, 2))
        f1 = fractal.copy().scale(np.true_divide(1, 2))
        f2 = fractal.copy().scale(np.true_divide(1, 2))

        # self.play(Create(t0),run_time=0.5)
        # self.play(Create(t1),run_time=0.5)
        # self.play(Create(t2),run_time=0.5)

        #self.play(ReplacementTransform(fractal,f0))
        self.play(f0.animate.align_to(fractal, DL), run_time=0.5)
        self.play(f1.animate.align_to(fractal, DR), run_time=0.5)
        self.play(f2.animate.align_to(fractal, UP), run_time=0.5)

        # fractal.apply_to_family(lambda x: x.reset_points())
        fractal.apply_to_family(lambda x: x.reset_points())

        fractal = Group(f0, f1, f2)
        gc.collect()

        # This is cool to visualize how the fractals scale but not quite what we want
        # self.clear()

        if count <= depth:
            count = count + 1
            return self.fractal(fractal, depth, count)
        return fractal
