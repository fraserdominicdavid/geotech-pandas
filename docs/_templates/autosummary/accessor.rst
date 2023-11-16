{{ fullname.split('.')[-1] | escape | underline }}

.. currentmodule:: {{ module.split('.')[0] }}

.. autoaccessor:: {{ (module.split('.')[1:] + [objname]) | join('.') }}

{%- block members %}
{%- if members %}

{{ _('Subaccessors') | escape | underline('-') }}

.. autosummary::
   :toctree:
   :template: autosummary/accessor_subaccessor.rst
{% for item in members if item[0] != "_" %}
   {{ name }}.{{ item }}
{%- endfor %}
{%- endif %}
{%- endblock %}