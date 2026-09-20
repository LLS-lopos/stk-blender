import bpy
from ...base.node_base import node


class STK_preview_cmd(node):
    bl_idname = 'STK_Preview_cmd'
    bl_label = 'Preview CMD'
    bl_icon = 'INFO'

    # Property to store the value to display
    doc: bpy.props.StringProperty(name="Value", description="Value to display",
        default="")

    def init(self, context):
        # Create input socket
        self.node_input("NodeSocketString", "preview_input", "preview", "")

    def draw_buttons(self, context, layout):
        # Display the value in the interface
        box = layout.box()
        formatted_text = self.format_text(self.doc)
        for ligne in formatted_text.split('\n'):
            box.label(text=ligne)

    def process(self, context, id, path):
        # Check for input socket linked status and retrieve the value
        if self.inputs[0].is_linked:
            self.doc = str(self.inputs[0].links[0].from_socket.default_value)
        else:
            self.doc = ""

        return self.doc

    def format_text(self, text):
        """Format the text by adding line breaks every 60 characters or 8 words."""
        words = text.split()
        formatted_lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word)

            # Check if adding the word exceeds the character or word limit
            if current_length + word_length + len(current_line) > 60 or len(current_line) >= 8:
                formatted_lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length

        # Add the last line if it's not empty
        if current_line:
            formatted_lines.append(' '.join(current_line))

        return '\n'.join(formatted_lines)

    def update(self):
        """Called when the node needs to be updated"""
        self.process(bpy.context, None, None)