from inspect import Signature, Parameter

# make a signature for a func(x, y=42, *, z=None)

params = [Parameter('x', Parameter.POSITIONAL_OR_KEYWORD),
          Parameter('y',Parameter.POSITIONAL_OR_KEYWORD,default=42),
          Parameter('z',Parameter.KEYWORD_ONLY,default=None)]

sig = Signature(params)
print(sig)