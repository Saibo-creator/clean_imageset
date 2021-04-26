# clean_imageset

A script using ArcFace age estimator to remove incorrectly labeled images

## Usage
1. use age estimator to remove incorrectly labeled images

To clean images in the `childhood/`, do 
```bash
python main.py -i childhood -o childhood_clean -e childhood_err -u childhood_unk
```

This will move estimate the age of the person in image and compare it with the label.
If the gap between the two is large, the image will be considered as incorrectly labeled 
adn the image will be moved to `childhood_err`, otherwise `childhood_clean`. For some case where the image
is corrupted or some other cases, it will be moved to `childhood_unk`



To deal with large images in the `large_img/`, do 
```bash
python main.py -i large_img -o childhood_clean -e childhood_err -u childhood_unk
```

⭕️This may cause your PC run out of memory and crash. 


2. normalise image filename
- remove space in filename
- replace filename with a uuid
- set the hierarchical file structure to a plat file structure
- replace "|" with "_" in the filename
- build a mapping table between original filename and the uuid

```python
python 
```


