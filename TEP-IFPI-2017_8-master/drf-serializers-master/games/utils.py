
def check_valid_list(list_var, keys):
	dict_fields = {}
	dict_fields = map(lambda x: {x : '%s eh requerido' % (x)}, filter(lambda x: list_var.get(x, None) is None or list_var.get(x, "") == "", keys))
	return dict_fields

def check_unique(model, data):
	return model.objects.filter(name = data).exists()