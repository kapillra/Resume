mymodels = ['Education', 'Experience', 'Master', 'Project', 'Reference', 'Skill', 'UserProfile', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'gender_choices', 'models', 'skill_level']

for m in mymodels:
    if m.startswith("__") and m.endswith("__"):
        continue
    print(m)