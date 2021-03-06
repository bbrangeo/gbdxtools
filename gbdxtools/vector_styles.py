from gbdxtools.vector_style_expressions import StyleExpression


class VectorStyle(object):
    """ Allows setting parameters common to all layer styles

        Args:
            opacity (float/StyleExpression/list):  the opacity of the circles (will accept either a float value, a
                    StyleExpression, or a list representing a mapbox-gl conditional expression)
            color (str/StyleExpression/list): the color of the circles (will accept either an an rgb/hex/html-color-name
                    string, a StyleExpression, or a list representing a mapbox-gl conditional expression)
            translate: (float): the offset from the original vector location at which the vector will be rendered
    """
    def __init__(self, opacity=1.0, color='rgb(255,0,0)', translate=None, **kwargs):
       
        self.opacity = opacity
        self.color = color
        self.translate = translate
        self.type = None

    @staticmethod
    def get_style_value(style_value):
        """
        Decides which value will be added to a style's 'paint' configuration

        Args:
            style_value: the value set on the style instance

        Returns:
            a value suitable for inclusion in a 'paint' configuration
        """
        if isinstance(style_value, StyleExpression):
            return style_value.expression
        else:
            return style_value

    def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl style entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript 'paint' snippet
        """
        raise NotImplementedError()


class CircleStyle(VectorStyle):
    """ Creates a style entry for a circle layer.

        See https://www.mapbox.com/mapbox-gl-js/style-spec/#layers-circle

        Args:
            radius (float/StyleExpression/list): the radius of the circles (will accept either a float value, a StyleExpression, or
                    a list representing a mapbox-gl conditional expression)
            opacity (float/StyleExpression/list):  the opacity of the circles (will accept either a float value, a StyleExpression, or
                    a list representing a mapbox-gl conditional expression)
            color (str/StyleExpression/list): the color of the circles (will accept either an an rgb/hex/html-color-name string,
                    a StyleExpression, or a list representing a mapbox-gl conditional expression)

        Returns:
            A circle style which can be applied to a circle layer
    """
    def __init__(self, radius=1.0, **kwargs):
        
        super(CircleStyle, self).__init__(**kwargs)
        self.radius = radius
        self.type = 'circle'

    def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl circle paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        snippet = {
            'circle-radius': VectorStyle.get_style_value(self.radius),
            'circle-opacity': VectorStyle.get_style_value(self.opacity),
            'circle-color': VectorStyle.get_style_value(self.color)
        }
        if self.translate:
            snippet['circle-translate'] = self.translate

        return snippet


class LineStyle(VectorStyle):
    """ Creates a style entry for a line layer

        See https://www.mapbox.com/mapbox-gl-js/style-spec/#layers-line

        Args:
            cap (str): the line-ending style ('butt' (default), 'round', or 'square')
            join (str): the line-joining style ('miter' (default), 'bevel', or 'round')
            width (float/StyleExpression/list): the width of the line in pixels
            gap_width (float/StyleExpression/list): the width of the gap between the line and its casing in pixels
            blur (float): blur value in pixels
            dasharray (list): list of numbers indicating line widths for a dashed line
            opacity (float/StyleExpression/list):  the opacity of the circles (will accept either a float value or
                      a list representing a mapbox-gl conditional expression)
            color (str/StyleExpression/list): the color of the circles (will accept either an an rgb/hex/html-color-name
                      string, a StyleExpression, or a list representing a mapbox-gl conditional expression)

        Returns:
            A line style which can be applied to a line layer
    """

    def __init__(self, cap='butt', join='miter', width=1.0, gap_width=0,
                 blur=0, dasharray=None, **kwargs):
        
        super(LineStyle, self).__init__(**kwargs)
        self.cap = cap
        self.join = join
        self.width = width
        self.gap_width = gap_width
        self.blur = blur
        self.dasharray = dasharray
        self.type = 'line'

    def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl line paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        # TODO Figure out why i cant use some of these props
        snippet = {
            'line-opacity': VectorStyle.get_style_value(self.opacity),
            'line-color': VectorStyle.get_style_value(self.color),
            #'line-cap': self.cap,
            #'line-join': self.join,
            'line-width': VectorStyle.get_style_value(self.width),
            #'line-gap-width': self.gap_width,
            #'line-blur': self.blur,
        }
        if self.translate:
            snippet['line-translate'] = self.translate

        if self.dasharray:
            snippet['line-dasharray'] = VectorStyle.get_style_value(self.dasharray)

        return snippet


class FillStyle(VectorStyle):
    """ Creates a style entry for a fill layer.

        See https://www.mapbox.com/mapbox-gl-js/style-spec/#layers-fill

        Args:
            opacity (float/StyleExpression/list):  the opacity of the circles (will accept either a float value, a
                        StyleExpression, or a list representing a mapbox-gl conditional expression)
            color (str/StyleExpression/list): the color of the fill (will accept either an an rgb/hex/html-color-name
                        string, a StyleExpression, or a list representing a mapbox-gl conditional expression)
            outline_color (str/StyleExpression/list): the color of the outline (will accept either an an
                        rgb/hex/html-color-name string, a StyleExpression, or a list representing a mapbox-gl
                        conditional expression)

        Returns:
            A fill style which can be applied to a fill layer
    """
    def __init__(self, color="rgb(255,0,0)", 
                       opacity=.5, 
                       outline_color=None,
                       **kwargs):
        
        super(FillStyle, self).__init__(**kwargs)
        self.outline_color = outline_color if outline_color is not None else color
        self.opacity = opacity
        self.color = color
        self.type = 'fill'

    def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl fill paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        snippet = {
            'fill-opacity': VectorStyle.get_style_value(self.opacity),
            'fill-color': VectorStyle.get_style_value(self.color),
            'fill-outline-color': VectorStyle.get_style_value(self.outline_color)
        }
        if self.translate:
            snippet['fill-translate'] = self.translate

        return snippet

class FillExtrusionStyle(FillStyle):
    """ Creates a style entry for extruded polygons (fills)

        See https://www.mapbox.com/mapbox-gl-js/style-spec/#layers-fill-extrusion

        Args:
            opacity (float/StyleExpression/list):  the opacity of the circles (will accept either a float value, a
                        StyleExpression, or a list representing a mapbox-gl conditional expression)
            color (str/StyleExpression/list): the color of the circles (will accept either an rgb/hex/html-color-name
                   string, a StyleExpression, or a list representing a mapbox-gl conditional expression)
            base (int/StyleExpression): the height at which to extrude the base of the features.
                                         must be less than or equal to the height.
            height (int/StyleExpression): the height with which to extrude features.

        Returns:
            A fill-extrusion style which can be applied to a fill-extrusion layer
    """

    def __init__(self, base=0, height=0, **kwargs):
        
        super(FillExtrusionStyle, self).__init__(**kwargs)
        self.base = base
        self.height = height
        self.type = 'fill-extrusion'

    def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl fill-extrusion paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        snippet = {
            'fill-extrusion-opacity': VectorStyle.get_style_value(self.opacity),
            'fill-extrusion-color': VectorStyle.get_style_value(self.color),
            'fill-extrusion-base': VectorStyle.get_style_value(self.base),
            'fill-extrusion-height': VectorStyle.get_style_value(self.height)
        }
        if self.translate:
            snippet['fill-extrusion-translate'] = self.translate

        return snippet

class HeatmapStyle(VectorStyle):
    """ Creates a style entry for heatmap layers.

        See https://www.mapbox.com/mapbox-gl-js/style-spec/#layers-heatmap

        Args:
            opacity (float/StyleExpression/list):  the opacity of the circles (will accept either a float value,
                        a StyleExpression, or a list representing a mapbox-gl conditional expression)
            radius (int): the radius of the circles (will accept either a float value, a StyleExpression, or
                        a list representing a mapbox-gl conditional expression)
            color (str/StyleExpression/list): the color of the circles (will accept either an rgb/hex/html-color-name
                        string, a StyleExpression, or a list representing a mapbox-gl conditional expression)
            intensity (int/StyleExpression): controls the intensity of the heatmap
            weight (int/StyleExpression): how much an individual point contributes to the heatmap

        Returns:
            A heatmap style which can be applied to a heatmap layer
    """

    def __init__(self, intensity=1, weight=1, color=None, radius=1, **kwargs):
        
        super(HeatmapStyle, self).__init__(**kwargs)
        if color is None:
            self.color = self.default_color
        else:
            self.color = color
        self.intensity = intensity
        self.weight = weight
        self.radius = radius
        self.type = 'heatmap'

    @property
    def default_color(self):
        return [
            "interpolate",
            ["linear"], ["heatmap-density"],
            0, "rgba(0, 0, 255, 0)",
            0.1, "royalblue",
            0.3, "cyan", 
            0.5, "lime",
            0.7, "yellow",
            1, "red"
        ]

    def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl heatmap paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        snippet = {
            'heatmap-radius': VectorStyle.get_style_value(self.radius),
            'heatmap-opacity': VectorStyle.get_style_value(self.opacity),
            'heatmap-color': VectorStyle.get_style_value(self.color),
            'heatmap-intensity': VectorStyle.get_style_value(self.intensity),
            'heatmap-weight': VectorStyle.get_style_value(self.weight)
        }

        return snippet
