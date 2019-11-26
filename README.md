# Triplets Dataset Generator for Street2Shop Dataset

Tools to create triplet pair dataset for [Street2Shop](http://www.tamaraberg.com/street2shop/) Dataset

<img src="/assets/street2shop.jpg" width="480">

# Requirements

* Install Python Packages
```
$ pip install -r requirements.txt
```

* Download and unzip pairs list file
```
$ curl -O http://www.tamaraberg.com/street2shop/wheretobuyit/meta.zip
$ unzip meta.zip
$ rm meta.zip
```

* **Download Street2Shop Dataset** <br/>
Check [my other repository](https://github.com/fadhilmch/street2shop-download) to download images from Street2Shop Dataset

# Usage


* Option 1: Make a triplet and randomly select one negative sample (Overwrite if output file already exist)

```sh
$ python tripletsGenerator.py --dataset_dir '../dataset/' --overwrite
```

* Option 2: Make a triplet and randomly select two negative sample (one from other class and one from inclass) (Overwrite if output file already exist)

```sh
$ python tripletsGenerator.py --dataset_dir '../dataset/' --inclass_neg --overwrite
```

* Option 3: Make a triplet and randomly select one negative sample from the two different negative classes (Overwrite if output file already exist)

```sh
$ python tripletsGenerator.py --dataset_dir '../dataset/' --overwrite --number_neg_class 2 
```

* Option 4: Make a triplet and randomly select two negative samples from the two different negative classes (Overwrite if output file already exist)

```sh
$ python tripletsGenerator.py --dataset_dir '../dataset/' --overwrite --number_neg_class 2 --number_neg_sample 2
```

* Extra: Running Options
```sh
  --dataset_dir             Path to images dataset [Required]
  --pair_dir                Path to pair meta file [Required]
  --output_file             Output file name and directory [default: /triplet_pairs.txt]
  --number_neg_class        Number of negative classes for negative sampling [default: 1]
  --number_neg_sample       Number of negative sample for each class in negative sampling [default:1]
  --overwrite               Overwrite the existed file
  --inclass_neg             Include negative sampling from the same class
  --split                   Split the dataset into train and val
```
