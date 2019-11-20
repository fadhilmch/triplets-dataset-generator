# Triplets Dataset Generator for Street2Shop Dataset

Tools to create triplet pair dataset for [Street2Shop](http://www.tamaraberg.com/street2shop/) Dataset

<img src="/assets/street2shop.jpg" width="480">

# Requirements

* Install Python Packages

```
$ pip install -r requirements.txt
```

* Download Street2Shop Dataset <br/>
Check [my other repository](https://github.com/fadhilmch/street2shop-download) to download images from Street2Shop Dataset

# Usage


* Option 1: Make a triplet and randomly select one negative sample (Overwrite if output file already exist)

```sh
$ python tripletsGenerator.py --dataset_dir '../street2shop-download/' --overwrite
```

* Option 2: Make a triplet and randomly select one negative sample from the two different negative classes (Overwrite if output file already exist)

```sh
$ python tripletsGenerator.py --dataset_dir '../street2shop-download/' --overwrite --number_neg_class 2 
```

* Option 3: Make a triplet and randomly select two negative samples from the two different negative classes (Overwrite if output file already exist)

```sh
$ python tripletsGenerator.py --dataset_dir '../street2shop-download/' --overwrite --number_neg_class 2 --number_neg_sample 2
```

* Extra: Running Options
```sh
  --dataset_dir             Path to images dataset [default: /images/]
  --output_file             Output file name and directory [default: /triplet_pairs.txt]
  --number_neg_class        Number of negative classes for negative sampling [default: 1]
  --number_neg_sample       Number of negative sample for each class in negative sampling [default:1]
  --overwrite               Overwrite the existed file
```
