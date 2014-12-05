import re


class MarkdownOutput:

    @staticmethod
    def array2row(input_array):
        return '|'.join(input_array)

    @staticmethod
    def array2table(input_array, header_included=True, justification='centered'):
        output_array = []
        # Blank header, if no header included
        if not header_included:
            header_row = [' '] * len(input_array[0])
            input_array.insert(0, header_row)
        # Header
        output_array.append(MarkdownOutput.array2row(input_array[0]))
        # Justification
        if justification.lower() is 'left':
            justification_string = ':-'
        elif justification.lower() is 'rightt':
            justification_string = '-:'
        else:
            justification_string = ':-:'
        output_array.append(re.sub('[^|]+',
                                   justification_string,
                                   MarkdownOutput.array2row(input_array[0])
                                   ))
        # Content
        for row in input_array[1:]:
            output_array.append(MarkdownOutput.array2row(row))
        return '\n'.join(output_array)

    @staticmethod
    def italicize(text):
        return "*{}*".format(text)

    @staticmethod
    def bold(text):
        return "**{}**".format(text)

    @staticmethod
    def bold_italicize(text):
        return "***{}***".format(text)

    @staticmethod
    def strikethru(text):
        return "~~{}~~".format(text)