{{ fullname.split('.')[2:] | join('.') | escape | underline }}

.. currentmodule:: {{ module.split('.')[0] }}

.. autoaccessorattribute:: {{ (module.split('.')[1:] + [objname]) | join('.') }}