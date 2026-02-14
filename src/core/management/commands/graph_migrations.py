from django.core.management import BaseCommand

# graph_models from django-extensions support 3 graph libraries:
# * pygraphviz: https://github.com/pygraphviz/pygraphviz
#   * Needed a PR for 3.14 support: https://github.com/pygraphviz/pygraphviz/pull/576
# * pydotplus: https://github.com/carlos-jenkins/pydotplus
# * pydot: https://github.com/pydot/pydot
#
# https://django-extensions.readthedocs.io/en/latest/graph_models.html#selecting-a-library
# https://github.com/django-extensions/django-extensions/blob/192b1d68ea720586b17e9ab7aa24ed0e9b2f38da/django_extensions/management/commands/graph_models.py#L15

# graph_models args:
# Creates a GraphViz dot file for the specified app names.
#
# positional arguments:
#   app_label
#
# options:
#   -h, --help            show this help message and exit
#   --app-style APP-STYLE
#                         Path to style json to configure the style per app
#   --pygraphviz          Output graph data as image using PyGraphViz.
#   --pydot               Output graph data as image using PyDot(Plus).
#   --dot                 Output graph data as raw DOT (graph description language) text data.
#   --json                Output graph data as JSON
#   --disable-fields, -d  Do not show the class member fields
#   --disable-abstract-fields
#                         Do not show the class member fields that were inherited
#   --display-field-choices
#                         Display choices instead of field type
#   --group-models, -g    Group models together respective to their application
#   --all-applications, -a
#                         Automatically include all applications from INSTALLED_APPS
#   --output, -o OUTPUTFILE
#                         Render output file. Type of output dependend on file extensions. Use png or jpg to render graph to image.
#   --layout, -l LAYOUT   Layout to be used by GraphViz for visualization. Layouts: circo dot fdp neato nop nop1 nop2 twopi
#   --theme, -t THEME     Theme to use. Supplied are 'original' and 'django2018'. You can create your own by creating dot templates in 'django_extentions/graph_models/themename/' template directory.
#   --verbose-names, -n   Use verbose_name of models and fields
#   --language, -L LANGUAGE
#                         Specify language used for verbose_name localization
#   --exclude-columns, -x EXCLUDE_COLUMNS
#                         Exclude specific column(s) from the graph. Can also load exclude list from file.
#   --exclude-models, -X EXCLUDE_MODELS
#                         Exclude specific model(s) from the graph. Can also load exclude list from file. Wildcards (*) are allowed.
#   --include-models, -I INCLUDE_MODELS
#                         Restrict the graph to specified models. Wildcards (*) are allowed.
#   --inheritance, -e     Include inheritance arrows (default)
#   --no-inheritance, -E  Do not include inheritance arrows
#   --hide-relations-from-fields, -R
#                         Do not show relations as fields in the graph.
#   --relation-fields-only RELATION_FIELDS_ONLY
#                         Only display fields that are relevant for relations
#   --disable-sort-fields, -S
#                         Do not sort fields
#   --hide-edge-labels    Do not show relations labels in the graph.
#   --arrow-shape {box,crow,curve,icurve,diamond,dot,inv,none,normal,tee,vee}
#                         Arrow shape to use for relations. Default is dot. Available shapes: box, crow, curve, icurve, diamond, dot, inv, none, normal, tee, vee.
#   --color-code-deletions
#                         Color the relations according to their on_delete setting, where it is applicable. The colors are: red (CASCADE), orange (SET_NULL), green (SET_DEFAULT), yellow (SET), blue (PROTECT), grey (DO_NOTHING), and purple (RESTRICT).
#   --rankdir {TB,BT,LR,RL}
#                         Set direction of graph layout. Supported directions: TB, LR, BT and RL. Corresponding to directed graphs drawn from top to bottom, from left to right, from bottom to top, and from right to left, respectively. Default is TB.
#   --ordering {in,out}   Controls how the edges are arranged. Supported orderings: "in" (incoming relations first), "out" (outgoing relations first). Default is None.
#   --version             Show program's version number and exit.
#   -v, --verbosity {0,1,2,3}
#                         Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
#   --settings SETTINGS   The Python path to a settings module, e.g. "myproject.settings.main". If this isn't provided, the DJANGO_SETTINGS_MODULE environment variable will be used.
#   --pythonpath PYTHONPATH
#                         A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".
#   --traceback           Display a full stack trace on CommandError exceptions.
#   --no-color            Don't colorize the command output.
#   --force-color         Force colorization of the command output.
#   --skip-checks         Skip system checks.

# Options that doesn't make sense with migration graph:
#   --disable-fields, -d  Do not show the class member fields
#   --disable-abstract-fields
#                         Do not show the class member fields that were inherited
#   --display-field-choices
#                         Display choices instead of field type
#   --verbose-names, -n   Use verbose_name of models and fields
#   --language, -L LANGUAGE
#                         Specify language used for verbose_name localization
#   --exclude-columns, -x EXCLUDE_COLUMNS
#                         Exclude specific column(s) from the graph. Can also load exclude list from file.
#   --exclude-models, -X EXCLUDE_MODELS
#                         Exclude specific model(s) from the graph. Can also load exclude list from file. Wildcards (*) are allowed.
#   --include-models, -I INCLUDE_MODELS
#                         Restrict the graph to specified models. Wildcards (*) are allowed.

# Selected options for migration graph:
#   -h, --help            show this help message and exit
#   --app-style APP-STYLE
#                         Path to style json to configure the style per app
#   --pygraphviz          Output graph data as image using PyGraphViz.
#   --pydot               Output graph data as image using PyDot(Plus).
#   --dot                 Output graph data as raw DOT (graph description language) text data.
#   --json                Output graph data as JSON
#   --group-models, -g    Group models together respective to their application
#   --all-applications, -a
#                         Automatically include all applications from INSTALLED_APPS
#   --output, -o OUTPUTFILE
#                         Render output file. Type of output dependend on file extensions. Use png or jpg to render graph to image.
#   --layout, -l LAYOUT   Layout to be used by GraphViz for visualization. Layouts: circo dot fdp neato nop nop1 nop2 twopi
#   --theme, -t THEME     Theme to use. Supplied are 'original' and 'django2018'. You can create your own by creating dot templates in 'django_extentions/graph_models/themename/' template directory.
#   --inheritance, -e     Include inheritance arrows (default)
#   --no-inheritance, -E  Do not include inheritance arrows
#   --hide-relations-from-fields, -R
#                         Do not show relations as fields in the graph.
#   --relation-fields-only RELATION_FIELDS_ONLY
#                         Only display fields that are relevant for relations
#   --disable-sort-fields, -S
#                         Do not sort fields
#   --hide-edge-labels    Do not show relations labels in the graph.
#   --arrow-shape {box,crow,curve,icurve,diamond,dot,inv,none,normal,tee,vee}
#                         Arrow shape to use for relations. Default is dot. Available shapes: box, crow, curve, icurve, diamond, dot, inv, none, normal, tee, vee.
#   --color-code-deletions
#                         Color the relations according to their on_delete setting, where it is applicable. The colors are: red (CASCADE), orange (SET_NULL), green (SET_DEFAULT), yellow (SET), blue (PROTECT), grey (DO_NOTHING), and purple (RESTRICT).
#   --rankdir {TB,BT,LR,RL}
#                         Set direction of graph layout. Supported directions: TB, LR, BT and RL. Corresponding to directed graphs drawn from top to bottom, from left to right, from bottom to top, and from right to left, respectively. Default is TB.
#   --ordering {in,out}   Controls how the edges are arranged. Supported orderings: "in" (incoming relations first), "out" (outgoing relations first). Default is None.
#   --version             Show program's version number and exit.
#   -v, --verbosity {0,1,2,3}
#                         Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
#   --settings SETTINGS   The Python path to a settings module, e.g. "myproject.settings.main". If this isn't provided, the DJANGO_SETTINGS_MODULE environment variable will be used.
#   --pythonpath PYTHONPATH
#                         A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".
#   --traceback           Display a full stack trace on CommandError exceptions.
#   --no-color            Don't colorize the command output.
#   --force-color         Force colorization of the command output.
#   --skip-checks         Skip system checks.


class Command(BaseCommand):
    pass
