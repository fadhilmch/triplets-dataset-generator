#!/usr/bin/python

import os
import re
import json
import pandas as pd
import itertools
import random
from argparse import ArgumentParser
from sklearn.model_selection import train_test_split


ext = 'jpg|jpeg|bmp|png|ppm|JPG|JPEG'


def get_files_list(directory_path, class_name=None):
    if class_name:
        return [file for root, _, files_list in os.walk(os.path.join(directory_path, class_name)) for file in files_list if re.match(r'([\w]+\.(?:' + ext + '))', file)]
    else:
        return [file for root, _, files_list in os.walk(directory_path) for file in files_list if re.match(r'([\w]+\.(?:' + ext + '))', file)]


def split_dataset(output_path, df):
    filename = output_path.split('/')[-1].split('.')[0]
    filepath = '/'.join(output_path.split('/')[:-1])
    train, val = train_test_split(df, test_size=0.3)
    train_file = filepath + 'train_' + filename + '.csv'
    val_file = filepath + 'val_' + filename + '.csv'
    train.to_csv(train_file, header=False, index=False)
    val.to_csv(val_file, header=False, index=False)
    return train_file, val_file


def main(args):
    if args.dataset_dir == None:
        raise ValueError(
            'Path to dataset directory is required!')
    print('Running program to sample triplet pair from Street2Shop Dataset...')
    images_path = args.dataset_dir
    classes_list = [dir_ for dir_ in os.listdir(
        images_path) if os.path.isdir(os.path.join(images_path, dir_))]

    # Handle error
    if len(classes_list) == 0:
        raise ValueError(
            'Your images directory does not contain class directories')
    if args.n_neg_class > len(classes_list)-1:
        raise ValueError(
            'The number of negative classes sample you want is exceeding the number of classes you have. Use smaller number of negative class samples')

    triplet_list = []
    count_pairs = {class_name: 0 for class_name in classes_list}

    for index, class_name in enumerate(classes_list):
        print('\n=======> Sampling triplet for class: ' + class_name)
        pair_file = 'meta/json/train_pairs_' + class_name + '.json'
        try:
            file_meta = open(pair_file, 'r')
        except ValueError:
            print("You don't have the pair file(s)")
        pair_data = json.load(file_meta)
        file_meta.close()
        neg_classes = random.sample([x for x in range(
            0, index)] + [x for x in range(index + 1, len(classes_list))], k=args.n_neg_class)
        neg_file_paths = [os.path.join(images_path, classes_list[neg_class])
                          for neg_class in neg_classes]
        n_neg_images = [len(get_files_list(x)) for x in neg_file_paths]

        if args.inclass_neg:
            inclass_path = os.path.join(images_path, class_name)
            n_inclass = len(get_files_list(inclass_path))

        print('Total images: ' + str(len(pair_data)) + ' images')
        existing_images = set(get_files_list(images_path, class_name))
        pair_data = list(filter(lambda data: str(
            data['photo']) + '.JPEG' in existing_images, pair_data))
        print('Total available images: ' +
              str(len(pair_data)) + ' images')
        pair_df = pd.DataFrame.from_dict(pair_data)
        product_list = pair_df['product'].unique()
        for product in product_list:
            pos_images = pair_df[pair_df['product']
                                 == product]['photo'].unique().tolist()
            com_images = list(itertools.combinations(pos_images, 2))
            for com in com_images:
                # Get index(s) of the image in class randomly
                neg_index_list = [[random.randint(
                    0, n_neg_image-1) for n in range(args.n_neg)] for n_neg_image in n_neg_images]

                # Handle inclass
                if args.inclass_neg:
                    for idx in range(args.n_neg):
                        temp_idx = random.randint(0, n_inclass-1)
                        while get_files_list(inclass_path)[temp_idx] in com:
                            temp_idx = random.randint(0, n_inclass-1)
                        temp_list = [class_name + '/' + str(img) + '.JPEG' for img in com] + [
                            class_name + '/' + get_files_list(inclass_path)[temp_idx]]
                        triplet_list.append(temp_list)
                        count_pairs[class_name] += 1

                for idx, class_index in enumerate(neg_index_list):
                    for neg_index in class_index:
                        temp_list = [class_name + '/' + str(img) + '.JPEG' for img in com] + [
                            neg_file_paths[idx].split('/')[-1] + '/' + get_files_list(neg_file_paths[idx])[neg_index]]
                        triplet_list.append(temp_list)
                        count_pairs[class_name] += 1
        print('Total triplet pairs: ' + str(count_pairs[class_name]))
    print('\nTotal new triplet pairs added: ' + str(sum(count_pairs.values())))
    cols = ['que', 'pos', 'neg']
    triplet_df = pd.DataFrame(triplet_list, columns=cols)

    if(args.split):
        train_path, val_path = split_dataset(args.output_file, triplet_df)
        print('\nSave train file to: ' + train_path)
        print('Save validation file to: ' + val_path)
    else:
        triplet_df.to_csv(args.output_file, header=False, index=False)
        print('\nSave file to: ' + args.output_file)


if __name__ == '__main__':
    parser = ArgumentParser()

    # Data handling parameters
    parser.add_argument('--dataset_dir', dest='dataset_dir',
                        type=str)
    parser.add_argument('--output_file', dest='output_file',
                        type=str, default='triplet_pairs.csv')
    parser.add_argument('--number_neg_class',
                        dest='n_neg_class', type=int, default=1)  # Number of negative classes for negative sampling
    parser.add_argument('--number_neg_sample',
                        dest='n_neg', type=int, default=1)  # Number of negative samples for each negative class
    parser.add_argument('--inclass_neg', dest='inclass_neg',
                        action='store_true')  # Include inclass negative sample
    parser.add_argument('--split', dest='split',
                        action='store_true')
    args = parser.parse_args()

    main(args)
    print('Finished')

    exit(0)
