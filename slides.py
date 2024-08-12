from manim import *  # or: from manimlib import *

from manim_slides import Slide
import random

def Item(*str,dot = True,font_size = 35,math=False,pw="8cm",color=WHITE):
    if math:
        tex = MathTex(*str,font_size=font_size,color=color)
    else:
        tex = Tex(*str,font_size=font_size,color=color,tex_environment=f"{{minipage}}{{{pw}}}")
    if dot:
        dot = MathTex("\\cdot").scale(2)
        dot.next_to(tex[0][0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    else:
        dot = MathTex("\\cdot",color=BLACK).scale(2)
        dot.next_to(tex[0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    g2 = VGroup()
    for item in tex:
        g2.add(item)

    return(g2)


def ItemList(*item,buff=MED_SMALL_BUFF):
    list = VGroup(*item).arrange(DOWN, aligned_edge=LEFT,buff=buff)
    return(list)

def Ray(start,end,ext:float=0,eext:float = 0,pos:float=0.5,color=BLUE):
    dir_lin = Line(start=start,end=end)
    dir = dir_lin.get_length()*ext*dir_lin.get_unit_vector()
    edir = dir_lin.get_length()*eext*dir_lin.get_unit_vector()
    lin = Line(start=start-edir,end=end+dir,color=color)
    arrow_start = lin.get_start()+pos*lin.get_length()*lin.get_unit_vector()
    arrow = Arrow(start=arrow_start-0.1*lin.get_unit_vector(),end=arrow_start+0.1*lin.get_unit_vector(),tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(lin,arrow)
    return ray

def CurvedRay(start,end,ext:float=0,radius=2,color=RED,rev = False):
    arc = ArcBetweenPoints(start=start,end=end,radius=radius,color=color)
    n = int(len(arc.get_all_points())/2)
    pt = arc.get_all_points()[n]
    pt2 = arc.get_all_points()[n+1]
    if rev:
        arrow = Arrow(start=pt2,end=pt,tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    else:
        arrow = Arrow(start=pt,end=pt2,tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(arc,arrow)
    return ray

def MyLabeledDot(label_in:Tex| None = None,label_out:Tex| None = None,pos:Vector = DOWN,shift=[0,0,0], point=ORIGIN,radius: float = DEFAULT_DOT_RADIUS,color = WHITE):
        if isinstance(label_in, Tex):
            radius = 0.02 + max(label_in.width, label_in.height) / 2
        
        dot = Dot(point=point,radius=radius,color=color)
        g1 = VGroup(dot)
        if isinstance(label_in, Tex):
            label_in.move_to(dot.get_center())
            g1.add(label_in)
        if isinstance(label_out, Tex):
            label_out.next_to(dot,pos)
            label_out.shift(shift)
            g1.add(label_out)

        return g1


class MyDashLabeledLine(DashedLine):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True  , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)

        if pos is None:
            mask  = Line(label.get_center()-0.6*label.width*self.get_unit_vector(),label.get_center()+0.6*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        self.add(label)

class MyLabeledLine(Line):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        if pos is None:
            if rot:
                mask  = Line(label.get_center()-0.65*label.width*self.get_unit_vector(),label.get_center()+0.65*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            else:
                mask  = Line(label.get_center()-0.65*label.height*self.get_unit_vector(),label.get_center()+0.65*label.height*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)
        self.add(label)


class MyLabeledArrow(MyLabeledLine, Arrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)

class MyDoubLabArrow(MyLabeledLine, DoubleArrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)





def ir(a,b): # inclusive range, useful for TransformByGlyphMap
    return list(range(a,b+1))


class LatexItems(Tex):
    def __init__(self, *args, page_width="15em", itemize="itemize",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{itemize}}}YourTextHere\end{{{itemize}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args, tex_template=template, tex_environment=None,font_size=font_size, **kwargs)


class AlignTex(Tex):
    def __init__(self, *args, page_width="15em",align="align*",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{cancel}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{align}}}YourTextHere\end{{{align}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args,font_size=font_size, tex_template=template, tex_environment=None, **kwargs)


class TransformByGlyphMap(AnimationGroup):
    def __init__(self, mobA, mobB, *glyph_map, replace=True, from_copy=True, show_indices=False, **kwargs):
		# replace=False does not work properly
        if from_copy:
            self.mobA = mobA.copy()
            self.replace = True
        else:
            self.mobA = mobA
            self.replace = replace
        self.mobB = mobB
        self.glyph_map = glyph_map
        self.show_indices = show_indices

        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []
        for from_indices, to_indices in self.glyph_map:
            print(from_indices, to_indices)
            if len(from_indices) == 0 and len(to_indices) == 0:
                self.show_indices = True
                continue
            elif len(to_indices) == 0:
                animations.append(FadeOut(
                    VGroup(*[self.mobA[0][i] for i in from_indices]),
                    shift = self.mobB.get_center()-self.mobA.get_center()
                ))
            elif len(from_indices) == 0:
                animations.append(FadeIn(
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    shift = self.mobB.get_center() - self.mobA.get_center()
                ))
            else:
                animations.append(Transform(
                    VGroup(*[self.mobA[0][i].copy() if i in mentioned_from_indices else self.mobA[0][i] for i in from_indices]),
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    replace_mobject_with_target_in_scene=self.replace
                ))
            mentioned_from_indices.extend(from_indices)
            mentioned_to_indices.extend(to_indices)

        print(mentioned_from_indices, mentioned_to_indices)
        remaining_from_indices = list(set(range(len(self.mobA[0]))) - set(mentioned_from_indices))
        remaining_from_indices.sort()
        remaining_to_indices = list(set(range(len(self.mobB[0]))) - set(mentioned_to_indices))
        remaining_to_indices.sort()
        print(remaining_from_indices, remaining_to_indices)
        if len(remaining_from_indices) == len(remaining_to_indices) and not self.show_indices:
            for from_index, to_index in zip(remaining_from_indices, remaining_to_indices):
                animations.append(Transform(
                    self.mobA[0][from_index],
                    self.mobB[0][to_index],
                    replace_mobject_with_target_in_scene=self.replace
                ))
            super().__init__(*animations, **kwargs)
        else:
            print(f"From indices: {len(remaining_from_indices)}    To indices: {len(remaining_to_indices)}")
            print("Showing indices...")
            super().__init__(
                Create(index_labels(self.mobA[0], color=PINK)),
                FadeIn(self.mobB.next_to(self.mobA, DOWN), shift=DOWN),
                Create(index_labels(self.mobB[0], color=PINK)),
                Wait(5),
                lag_ratio=0.5
                )


class Obj(Slide):
    def construct(self):
        title = Title('CHAPTER 3 : CURRENT ELECTRICITY',font_size=40,color=GREEN,match_underline_width_to_text=True)
        self.play(Write(title))
        #self.play(Rotate(title,2*PI))
        self.next_slide()
        Outline = Tex('LEARNING OBJECTIVES :',color=BLUE)
        self.play(Write(Outline))
        self.next_slide()
        self.play(Outline.animate.scale(0.75).next_to(title,DOWN,buff=0.5).to_edge(LEFT,buff=0.1))
        self.next_slide()
        list = BulletedList('ELECTRIC CURRENT',r' ELECTRIC CURRENTS IN\\ CONDUCTORS',r"OHM'S LAW, RESISTANCE",r'CURRENT DENSITY',r'DRIFT VELOCITY',r'RELATION BETWEEN CURRENT\\ AND DRIFT VELOCITY',
                            r'RESISTIVITY AND CONDUCTIVITY',r'MOBILITY').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.1*RIGHT)
        
        for i in range(len(list)):
            list.fade_all_but(i)
            self.play(Write(list[i]))
            self.next_slide()
    
        list2 = BulletedList(r"LIMITATIONS OF OHM'S LAW",r'TEMPERATURE DEPENDENCE\\ OF RESISTIVITY','ELECTRICAL ENERGY, POWER','CELLS, EMF, INTERNAL RESISTANCE',
                             'CELLS IN SERIES AND IN PARALLEL',"KIRCHHOFF'S RULES",r"WHEATSTONE BRIDGE").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        
        for i in range(len(list2)):
            list2.fade_all_but(i)
            self.play(Write(list2[i]))
            self.next_slide()
        list2.fade()
        list.fade_all_but(0)
        self.next_slide(loop=True)
        self.play(FocusOn(list[0]))
        self.play(Circumscribe(list[0]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('ELECTRIC CURRENT', color=BLUE)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()

class Current(Slide):
    def construct(self):
        Intro_title = Title('ELECTRIC CURRENT (I)', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True).to_corner(UL,buff=0.1)
        self.add(Intro_title)
        self.next_slide()
        steps1 = ItemList(Item(r"Charges in motion constitute an electric current.",pw="13 cm",color=GREEN),
                          Item(r"Current is defined as the rate of flow of electric charge through any cross-section of a conductor.",pw="13 cm",color=GREEN),
                          Item(r"For steady current(or average current) : $I=\dfrac{\text{total charge flowing }(\Delta q)}{\text{time taken} \Delta t}=\dfrac{ne}{t}$",pw="13 cm",color=GREEN),
                          Item(r"Currents are not always steady and hence more generally, we define the current as follows",pw="13 cm",color=GREEN),
                          Item(r"The current at time t (instantaneous current) across the cross-section of the conductor is defined as the value of the ratio of $\Delta Q$ to $\Delta t$ in the limit of $\Delta t$ tending to zero,",pw="13 cm",color=ORANGE),
                          Item(r"Instantaneous current : $\displaystyle I(t)=\lim_{\Delta x \to 0}\dfrac{ \Delta q}{\Delta t}=\dfrac{dQ}{dt}$",pw="13 cm",color=GREEN),
                          buff=0.45).next_to(Intro_title,DOWN).to_edge(LEFT).set_z_index(2)
        
        for item in steps1:
            self.play(Write(item))
            self.next_slide()

class Ex1(Slide):
    def construct(self):

        ex_title = Tex(r"Example 1 :", r" How many electrons pass through a lamp in 1 min, if the current is 300 mA? Given, the charge on an electron is $1.6\times 10^{-19}$ C",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))

class Ex2(Slide):
    def construct(self):

        ex_title = Tex(r"Example 2 :", r" The current in a device varies with time $t$ as $I=6t$, where $I$ is mA an t is in s. The amount of charge that passes through the device during $t=0$ s to $t=3$ s is- [CBSE 2023]",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))

class Ex3(Slide):
    def construct(self):

        ex_title = Tex(r"Example 3 :", r" (a) Estimate the average drift speed of conduction electrons in a copper wire of cross-sectional area $1.0 \times 10^{-7}\ m^2$ carrying a current of 1.5 A. Assume that each copper atom contributes roughly one conduction electron. The density of copper is $9.0 \times 10^3\ kg/m^33$, and its atomic mass is 63.5 u. (b) Compare the drift speed obtained above with, (i) thermal speeds of copper atoms at ordinary temperatures, (ii) speed of propagation of electric field along the conductor which causes the drift motion. [NCERT EXAMPLE]",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))

class Ex4A(Slide):
    def construct(self):

        ex_title = Tex(r"Example 4 :", r" (a) In Example 3.1, the electron drift speed is estimated to be only a few mm s$^{-1}$ for currents in the range of a few amperes? How then is current established almost the instant a circuit is closed? [NCERT EXAMPLE]",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.wait()
        self.next_slide()
        ex_sol = Tex(r"Solution :", r" Electric field is established throughout the circuit, almost instantly (with the speed of light) causing at every point a local electron drift. Establishment of a current does not have to wait for electrons from one end of the conductor travelling to the other end. However, it does take a little while for the current to reach its steady value.",tex_environment="{minipage}{13 cm}",font_size=35, color=PINK).next_to(ex_title,DOWN).to_corner(LEFT,buff=0.2)
        ex_sol[0].set_color(ORANGE)
        self.play(Write(ex_sol))


class Ex4B(Slide):
    def construct(self):

        ex_title = Tex(r"Example 4 :", r"(b)  The electron drift arises due to the force experienced by electrons in the electric field inside the conductor. But force should cause acceleration. Why then do the electrons acquire a steady average drift speed?",tex_environment="{minipage}{13 cm}",font_size=35, color=PINK).to_corner(UL,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.wait()
        self.next_slide()
        ex_sol = Tex(r"Solution :", r" Each 'free' electron does accelerate, increasing its drift speed until it collides with a positive ion of the metal. It loses its drift speed after collision but starts to accelerate and increases its drift speed again only to suffer a collision again and so on. On the average, therefore, electrons acquire only a drift speed.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).next_to(ex_title,DOWN).to_corner(LEFT,buff=0.2)
        ex_sol[0].set_color(ORANGE)
        self.play(Write(ex_sol))
    

class Ex4C(Slide):
    def construct(self):

        ex_title = Tex(r"Example 4 :", r"((c) If the electron drift speed is so small, and the electron's charge is small, how can we still obtain large amounts of current in a conductor?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UL,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.wait()
        self.next_slide()
        ex_sol = Tex(r"Solution :", r" Simple, because the electron number density is enormous, $\approx 10^{29} m^{-3}$.",tex_environment="{minipage}{13 cm}",font_size=35, color=PINK).next_to(ex_title,DOWN).to_corner(LEFT,buff=0.2)
        ex_sol[0].set_color(ORANGE)
        self.play(Write(ex_sol))

class Ex4D(Slide):
    def construct(self):

        ex_title = Tex(r"Example 4 :", r"((d)  When electrons drift in a metal from lower to higher potential, does it mean that all the 'free' electrons of the metal are moving in the same direction?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UL,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.wait()
        self.next_slide()
        ex_sol = Tex(r"Solution :", r" By no means. The drift velocity is superposed over the large random velocities of electrons.",tex_environment="{minipage}{13 cm}",font_size=35, color=PINK).next_to(ex_title,DOWN).to_corner(LEFT,buff=0.2)
        ex_sol[0].set_color(ORANGE)
        self.play(Write(ex_sol))

class Ex4E(Slide):
    def construct(self):

        ex_title = Tex(r"Example 4 :", r"((e)  Are the paths of electrons straight lines between successive collisions (with the positive ions of the metal) in the (i) absence of electric field, (ii) presence of electric field?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UL,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.wait()
        self.next_slide()
        ex_sol = Tex(r"Solution :", r" In the absence of electric field, the paths are straight lines; in the presence of electric field, the paths are, in general, curved.",tex_environment="{minipage}{13 cm}",font_size=35, color=PINK).next_to(ex_title,DOWN).to_corner(LEFT,buff=0.2)
        ex_sol[0].set_color(ORANGE)
        self.play(Write(ex_sol))

class Ex5(Slide):
    def construct(self):

        ex_title = Tex(r"Example 5 :", r" A heating element using nichrome connected to a 230 V supply draws an initial current of 3.2 A which settles after a few seconds to a steady value of 2.8 A. What is the steady temperature of the heating element if the room temperature is 27.0 $^\circ C$? Temperature coefficient of resistance of nichrome averaged over the temperature range involved is $1.70 \times 10^{-4}\ ^\circ C^{-1}$. [NCERT]",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))

class Ex6(Slide):
    def construct(self):

        ex_title = Tex(r"Example 6 :", r" A resistance coil is made by joining in parallel two resistances each of 10 $\Omega$. An emf of 1 V is applied between the two ends of coil for 5 min. Calculate the heat produced in calories.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))

class Ex7(Slide):
    def construct(self):

        ex_title = Tex(r"Example 7 :", r" Two bulbs are marked 220V-100W and 220V-50W, respectively. They are connected in series to 220 V mains. Determine the ratio of heat generated in them.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))

class Ex8(Slide):
    def construct(self):

        ex_title = Tex(r"Example 8 :", r" Two electric bulbs P and Q have their resistances in the ratio of $1:2$. They are connected in series across a battery. Find the ratio of the power dissipation in these bulbs. [CBSE 2018] ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
