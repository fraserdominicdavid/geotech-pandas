{{ fullname.split('.')[2:] | join('.') | escape | underline }}

.. currentmodule:: {{ module.split('.')[0] }}

.. autoaccessorcallable:: {{ (module.split('.')[1:] + [objname]) | join('.') }}

{% block methods -%}
{% if methods -%}
{{ _('Methods') | escape | underline('-') }}

.. autosummary::
   :toctree:
   :template: autosummary/accessor_method.rst
{% for item in methods %}
{#- This is needed to filter out private methods -#}
{% if item[0] != "_" %}
   {{ name }}.{{ item }}
{%- endif %}
{%- endfor %}
{%- endif %}
{%- endblock %}

{% block attributes -%}
{% if attributes -%}
{{ _('Attributes') | escape | underline('-') }}

.. autosummary::
   :toctree:
   :template: autosummary/accessor_attribute.rst
{% for item in attributes %}
   {{ name }}.{{ item }}
{%- endfor %}
{%- endif %}
{%- endblock %}