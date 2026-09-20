__all__ = ("Gradient",)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import RenderContext
from kivy.core.window import Window
from kivy.clock import mainthread
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, ColorProperty

shader_code = '''
#ifdef GL_ES
    precision highp float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_position;
uniform float u_angle;
uniform bool u_circular;
uniform vec4 u_color_start;
uniform vec4 u_color_end;

void main() {
    // Normalized coordinates (0–1)
    vec2 uv = (gl_FragCoord.xy - u_position) / u_resolution;

    // Convert angle to radians
    float rad = radians(u_angle);

    // Move origin to center and fix aspect ratio
    vec2 centered = uv - 0.5;
    float mixValue;

    if (!u_circular) {
        centered.x *= u_resolution.x / u_resolution.y;

        // Direction vector of gradient
        vec2 direction = vec2(cos(rad), sin(rad));

        // Linear projection onto gradient direction
        mixValue = dot(centered, direction) + 0.5;
    } else {
        // Rotation matrix
        mat2 rotation = mat2(cos(rad), -sin(rad),
                             sin(rad),  cos(rad));
        vec2 rotated = rotation * centered + 0.5;
        mixValue = distance(rotated, vec2(0.0, 1.0));
    }

    // Blend the colors
    vec4 finalColor = mix(u_color_start, u_color_end, clamp(mixValue, 0.0, 1.0));

    gl_FragColor = finalColor;
}
'''


class Gradient(Widget):
    """
    Represents a gradient widget capable of rendering a smooth transition between
    two colors, either linearly or circularly. This class provides fine-grained
    control over the gradient's appearance through adjustable properties such
    as angle, start color, end color, and whether the gradient should be circular.

    The class uses a custom `RenderContext` for rendering, enabling the application
    of fragment shaders to create high-performance gradient effects.

    :ivar angle: The angle of the gradient in degrees. Defaults to 90 degrees.
    :type angle: float
    :ivar color_start: The RGBA start color of the gradient. Defaults to [0, 0, 0, 0].
    :type color_start: list[float]
    :ivar color_end: The RGBA end color of the gradient. Defaults to [0, 0, 0, 0].
    :type color_end: list[float]
    :ivar circular: Indicates whether the gradient is circular. Defaults to False.
    :type circular: bool
    """
    angle = NumericProperty(90)
    color_start = ColorProperty([0, 0, 0, 0])
    color_end = ColorProperty([0, 0, 0, 0])
    circular = BooleanProperty(False)

    def __init__(self, **kwargs):
        # Use a RenderContext instead of normal canvas
        super().__init__(**kwargs)
        self.canvas = RenderContext(
            use_parent_projection=True,
            use_parent_modelview=True,
            fs=shader_code,
        )
        fbind = self.fbind
        fbind("angle", self._update_shader)
        fbind("color_start", self._update_shader)
        fbind("color_end", self._update_shader)
        fbind("circular", self._update_shader)
        fbind("size", self._update_shader)
        fbind("pos", self._update_shader)

        # with self.canvas:
        #     self.rect = Triangle(points=[0, 0, Window.width/2, Window.height, Window.width, 0])
        self._setup()

    @mainthread
    def _setup(self, *args):
        self._update_shader()

    # def on_size(self, *args):
    #     self.canvas['u_resolution'] = list(map(float, self.size))

    def _update_shader(self, *args):
        self.canvas['u_angle'] = float(self.angle)
        self.canvas['u_color_start'] = list(map(float, self.color_start))
        self.canvas['u_color_end'] = list(map(float, self.color_end))
        self.canvas['u_circular'] = int(self.circular)
        self.canvas['u_resolution'] = list(map(float, self.size))
        self.canvas['u_position'] = list(map(float, self.pos))


if __name__ == '__main__':
    from kivy.graphics import Rectangle

    class ShaderGradientApp(App):
        def build(self):
            d = Gradient()
            with d.canvas:
                rect = Rectangle(size=Window.size, pos=(0, 0))
            Window.bind(size=lambda _, s: setattr(rect, 'size', s))
            return d

    ShaderGradientApp().run()
