import albumentations as albu


def create_transform(aug_fn, size=None, normalize=True, bboxes=True, label_field='category_id', mean='imagenet',
                     std='imagenet', min_visibility=0.):
    pipeline = []

    if size:
        if isinstance(size, int):
            size = (size, size)

        resize_fn = albu.Resize(*size)
        aug_fn.insert(0, resize_fn)

    bbox_params = {
        'format': 'coco',
        'min_visibility': min_visibility,
        'label_fields': [label_field]
    } if bboxes else {}
    aug_fn = albu.Compose(aug_fn, bbox_params=bbox_params)
    pipeline.append(aug_fn)

    if normalize:
        mean, std = _get_mean_std(mean, std)
        normalize_fn = albu.Normalize(mean=mean, std=std)
        pipeline.append(normalize_fn)

    pipeline = albu.Compose(pipeline)
    return pipeline


def _get_mean_std(mean, std):
    if mean == 'imagenet':
        mean = [0.485, 0.456, 0.406]
    if std == 'imagenet':
        std = [0.229, 0.224, 0.225]
    return mean, std
