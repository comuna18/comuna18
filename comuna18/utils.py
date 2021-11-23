import uuid

def generate_random_slug(model, exclude_slugs=[]):
	while True:
		random_slug = uuid.uuid4().hex[:model.SLUG_LENGTH].upper()
		others = model.objects.filter(random_slug=random_slug)
		if others.count() == 0:
			if random_slug not in exclude_slugs:
				return random_slug
		break
