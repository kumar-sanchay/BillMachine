from django import template

register = template.Library()


class GlobalVariable:
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

    def get_var(self):
        return self.varname

    def get_value(self):
        return self.value

    def set_val(self, value):
        self.value = value


class GlobalVariableSet(template.Node):
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

    def render(self, context):
        gc = context.get(self.varname, None)
        if gc is not None:
            gc.set_val(self.value)
        else:
            context[self.varname] = GlobalVariable(
                varname=self.varname,
                value=self.value
            )
        return ''


@register.tag(name="set_global")
def set_global(parser, token):
    try:
        tag, varname, value = token.contents.split(None, 2)
    except ValueError:
        raise template.TemplateSyntaxError(
            "{} excepts 2 arguements".format(token.contents.split()[0])
        )
    return GlobalVariableSet(varname, value)


class GlobalVariableGet(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        gc = context.get(self.varname, None)
        if gc is not None:
            return str(gc.get_value())
        return ''


@register.tag(name="get_global")
def get_global(parser, token):
    try:
        tag, varname = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            '{} error'.format(token.contents.split()[0])
        )
    return GlobalVariableGet(varname=varname)


class GlobalVariableIncrement(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        gc = context.get(self.varname, None)
        if gc is not None:
            gc.set_val(int(gc.get_value()) + 1)
            return ''
        else:
            return ''


@register.tag(name="increment_global")
def increment_global(parser, token):
    try:
        tag, varname = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "{} error".format(token.contents.split()[0])
        )
    return GlobalVariableIncrement(varname=varname)


@register.filter
def index(lst: list, val):
    return lst.index(val)