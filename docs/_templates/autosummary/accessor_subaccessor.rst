{{ fullname.split('.')[2:] | join('.') | escape | underline }}

.. currentmodule:: {{ module.split('.')[0] }}

.. autoaccessorcallable:: {{ (module.split('.')[1:] + [objname]) | join('.') }}

{%- block members %}
{%- for item in members if item not in methods and item not in attributes and item[0] != "_" %}
{%- if loop.length > 0 %}
{%- if loop.index == 1 %}

{{ _('Subaccessors') | escape | underline('-') }}

.. autosummary::
   :toctree:
   :template: autosummary/accessor_subaccessor.rst
{% endif %} 
   {{ name }}.{{ item }}
{%- endif %}
{%- endfor %}
{%- endblock %}

{%- block methods %}
{%- for item in methods if methods and item[0] != "_" %}
{%- if loop.length > 0 %}
{%- if loop.index == 1 %}

{{ _('Methods') | escape | underline('-') }}

.. autosummary::
   :toctree:
   :template: autosummary/accessor_method.rst
{% endif %}
   {{ name }}.{{ item }}
{%- endif %}
{%- endfor %}
{%- endblock %}

{%- block attributes %}
{%- if attributes %}

{{ _('Attributes') | escape | underline('-') }}

.. autosummary::
   :toctree:
   :template: autosummary/accessor_attribute.rst
{% for item in attributes %}
   {{ name }}.{{ item }}
{%- endfor %}
{%- endif %}
{%- endblock %}