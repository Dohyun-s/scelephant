# # %% CORE %%
# # import internal modules

"""
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
This part should be uncommented in core.py
"""

from .utils import *
from .misc import *
from . import biobookshelf as bk
from . import BA
from . import STR

"""
||||||||||||||||||||||||||||||||
"""

# from scelephant.core import *
# from biobookshelf import BA
# from biobookshelf import STR
# import biobookshelf as bk
# bk.Wide( 100 )

"""
This part should be uncommented in jupyter notebook
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""

from typing import Union, List, Literal, Dict, Callable, Set, Iterable, Tuple
import os
import pandas as pd
import numpy as np
import multiprocessing as mp
import math
import logging
from copy import deepcopy
import pickle
import time
import glob
import gzip  # to handle gzip file
import shutil  # for copying file
import base64  # for converting binary to text data (web application)
import json  # to read and write JSON file
import matplotlib.pyplot as plt
import scipy.sparse
import io
import concurrent.futures  # for multiprocessing

pd.options.mode.chained_assignment = None  # default='warn' # to disable worining

# SCElephant is currently implemented using Zarr
import zarr
import numcodecs
from bitarray import bitarray  ## binary arrays

import shelve  # for persistent database (key-value based database)

from tqdm import tqdm as progress_bar  # for progress bar

# from tqdm.autonotebook import tqdm  as progress_bar # for progress bar with jupyter notebook integration # not compatible with multi-processing

# # for handling s3 objects
# import s3fs

# set logging format
logging.basicConfig(
    format="%(asctime)s [%(name)s] <%(levelname)s> (%(funcName)s) - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("SC-Elephant")

# define version
_version_ = "0.1.0"
_scelephant_version_ = _version_
_last_modified_time_ = "2023-05-06 11:40:22"

str_release_note = [
    """
    # %% RELEASE NOTE %%
    # 2022-07-21 10:35:42 
    HTTP hosted RamData subclustering tested and verified.
    identified problems: Zarr HTTP Store is not thread-safe (crashes the program on run time) nor process-safe (dead lock... why?).
    Therefore, serializing access to Zarr HTTP Store is required 

    if these implementations are in place, subclustering on HTTP-hosted RamData will be efficient and accurate.

    # 2022-07-28 16:00:50 

    Hard dependency on entries sorted by string representations ('id_feature' and 'id_cell') will be dropped. 
    This decision was made to make integration of datasets (especially datasets fetched from the web with dataset exists locally) more efficient.
    Also, this change will make the RamData construction process more time- and memory-efficient

    Also, hard dependency on feature/barcode sorted ramtx will be dropped, and a new ramtx, dense ramtx will be introduced

    # 2022-07-30 17:24:25 
    metadata naming convention changed, removing backward compatibility.

    dense ramtx was introduced, and the dependency on the existence of a paired sparse ramtx object was dropped. 
    below is a short description about the different types of ramtx objects:

        # 'mode' of RAMtx objects
        There are three valid 'mode' (or internal structures) for RAMtx object : {'dense' or 'sparse_sorted_by_barcodes', 'sparse_sorted_by_features'}

        (sparse_sorted_by_barcodes) <---> (dense) <---> (sparse_sorted_by_features)
        *fast barcode data retrieval                    *fast feature data retrieval

        As shown above, RAMtx objects are interconvertible. Of note, for the converion between sparse ramtx sorted by barcodes and features, 'dense' ramtx object should be used in the conversion process.
        - dense ramtx object can be used to retrieve data of a single barcode or feature (with moderate efficiency)
        - sparse ramtx object can only be used data of either a single barcode ('sparse_sorted_by_barcodes') or a single feature ('sparse_sorted_by_features') very efficiently.

    # 2022-08-01 20:38:54 

    RamData.apply has been implemented
    RAMtx.__getitem__ function has been improved to allow read data respecting chunk boundaries
    RAMtx.batch_generator now respect chunk boundaries when creating batches

    # 2022-08-03 00:39:12 
    wrote a method in RamData for fast exploratory analysis of count data stored in dense, which enables normalizations/scaling of highly/variable genes of 200k single-cell data in 3~4 minutes from the count data
    now ZarrDataFrame supports multi-dimensional data as a 'column'
    also, mask, coordinate array, and orthogonal selections (all methods supported by Zarr) is also supported in ZarrDataFrame.

    # 2022-08-05 01:53:22 
    RAMtx.batch_generator was modified so that for dense matrix, appropriate batch that does not overwhelm the system memory
    RamData.apply was modified to allow synchronization across processes. it is a bit slow than writing chunks by chunk, but consums far less memory.

    # 2022-08-05 17:24:17 
    improved RamData.__getitem__ method to set obsm and varm properties in the returned AnnData object

    # 2022-08-05 17:42:03 
    RamData dimension reduction methods were re-structured

    # 2022-08-06 22:24:19 
    RamData.pca was split into RamData.train_pca and RamData.apply_pca

    # 2022-08-07 03:15:06 
    RAMtx.batch_generator was modified to support progress_bar functionality (backed by 'tqdm')
    RAMtx.get_total_num_records method was added to support progress_bar functionality (backed by 'tqdm')

    # 2022-08-07 17:00:53 
    RamData.umap has been split into RamData.train_umap and RamData.apply_umap

    # 2022-08-08 00:49:58 
    RamData._repr_html_ was added for more interactive visualization of RamData in an interactive IPython environment (such as Jupyter Notebook).

    # 2022-08-08 23:14:16 
    implemented PyNNdescent-backed implementation of cluster label assignments using labels assigned to subsampled barcodes, adding RamData.

    # 2022-08-09 03:13:15 
    implemented leiden clustering algorithm using 'leidenalg.find_partition' method

    # 2022-08-10 04:51:54 
    implemented subsampling method using iterative community detection and density-based subsampling algorithms (RamData.subsample)

    # 2022-08-10 10:02:18 
    RamData.delete_model error corrected

    # 2022-08-12 01:51:27 
    resolved error in RamData.summarize

    # 2022-08-16 02:32:51 
    resolved RAMtx.__getitem__ performance issues for dense RAMtx data when the length of axis not for querying is extremely large.
    New algorithm uses sub-batches to convert dense matrix to sparse matrix in a memory-efficient conversion.

    # 2022-08-16 11:21:53 
    resolved an issue in RAMtx.survey_number_of_records_for_each_entry

    # 2022-08-18 15:30:22 
    bumped version to v0.0.5

    # 2022-08-21 16:13:08 
    RamData.get_expr function was implemented.
        possible usages: (1) calculating gene_set/pathway activities across cells, which can subsequently used for filtering cells for subclustering
                         (2) calculating pseudo-bulk expression profiles of a subset of cells across all active features 

    # 2022-08-23 11:36:32 
    RamData.find_markers : finding markers for each cluster using AUROC, log2fc, and statistical test methods in memory-efficient method, built on top of RamData.summarize
    RamData.get_marker_table : retrieve markers as table from the results produced by 'RamData.find_markers'

    # 2022-08-25 16:18:04 
    initialized ZarrDataFrame class with an additional functionality (combined mode)

    # 2022-08-27 10:21:45 
    ZarrDataFrame class now support combined mode, where data are retrieved across multiple zdf conmponents, either sharing rows ('interleaved' type) or each has unique rows ('stacked' type).
    currently supported operations are __getitem__
    Also, fill_value of categorical column is now -1, interpreting empty values as np.nan by default

    # 2022-08-29 12:46:18 
    RamDataAxis now supports combined mode, either sharing rows ('interleaved' type) or each has unique rows ('stacked' type), backed by the combined ZarrDataFrame object.
    RamDataAxis can automatically determines combined type, and build index mapping dictionaries for the 'interleaved' type.

    # 2022-09-05 23:49:37
    RAMtx, RamDataLayer, RamData now supports combined mode.
    RamData.load_model now can search and download models from component RamData

    # 2022-09-06 20:21:27 
    multiprocessing and load-balancing algorithm was improved (biobookshelf.bk.Multiprocessing_Batch_Generator_and_Workers)

    # 2022-09-07 21:13:29 
    a multiprocessing support for HTTP-stored RamData objects was implemented by hosting zarr objects in spawned processes, making them thread-safe by isolating zarr objects from each other.

    # 2022-09-08 18:18:13 
    RamDataAxis.select_component method was added.

    # 2022-09-09 14:58:02 
    RamDataAxis.iterate_str method was added 

    # 2022-09-11 23:53:36 
    ZarrDataFrame.lazy_load method draft implementation completed 

    # 2022-09-12 15:51:48 
    - lazy loading implementation for remotely-located combined ZarrDataFrame :
        combined ZarrDataFrame should be optimized more. When only a subset of data is needed, a filter will be assigned to combined column indicating which entry contains data and data of entries will be downloaded as it is accessed (lazy loading). 
    - lazy loading implementation of string representation of Axis objects :
        similar mechanism to ZarrDataFrame's lazy-loading will be used

    # 2022-09-12 17:50:10 
    RamDataAxis object will be no longer modify filter using current RamDataLayer's active entries

    # 2022-09-14 10:11:34 
    - KNN models will be combined in to a single model, and associated filter and column name will be saved together in order to check validity of the model.
    - RamData.train_knn method was implemented, for building knnindex using the given X
    - RamData.apply_knn method was implemented for knnindex-based embedding and classification

    # 2022-09-15 22:06:09 
    - RamData.train_dl method was implemented, for training deep-learning based model for classification/embedding tasks
    - RamData.apply_dl method was implemented, for applying the trained deep-learning model across the entries

    # 2022-09-18 01:00:28 
    - an issue in the RAMtx.get_fork_safe_version method was resolved (mask was not properly set)
    - RamData.get_model_path method was implemented. it uses recursive solution for retrieving (remote) path of the given model from components and masks
    - RamData.load_model method was re-implemented using RamData.get_model_path
    - RamData.prepare_dimension_reduction_from_raw was modified to support fast embedding of barcodes of the non-reference RamData components with the reference barcodes of the reference RamData component.

    # 2022-09-18 16:54:20 
    - an issue in the RamData.load_model resolved.

    # 2022-09-24 11:46:09 
    - RamData.apply_knn method 'embedder' algorithm was improved in order to avoid averaging embeddings of very distant 'neighbors'. standard deviations of embedding of the neighbors are used to identify outliers

    # 2022-09-24 22:20:38 
    finalized version of 0.0.7 released

    # 2022-10-19 13:16:19 
    combined RamData will exclude RAMtx of the reference RamData for weight calculation / data retrieval
        - RAMtx.survey_number_of_records_for_each_entry was updated

    # 2022-10-29 18:08:59 
    RamData.subset draft implementation completed
    RamData.apply was updated so that file I/O operations on sparse matrix will be off-loaded to a seperate process for asynchronous operations. (much faster since main process will not be blocked from distributing works in order to post-process sparse matrix outputs)

    # 2022-10-29 23:57:53 
    RamDataAxis.update, RamDataAxis.get_df methods were implemented, and ZarrDataFrame.update and ZarrDataFrame.get_df methods were re-implemented.

    # 2022-10-30 18:05:30 
    ZarrDataFrame.__setitem__ method updated for processing categorical data

    # 2022-11-08 19:34:38 
    RamData.apply_knn embedding algorithm was improved so that outliers are detected using the distance from the closest point.

    # 2022-11-17 13:53:56 
    an error in RamData.apply_knn resolved

    # 2022-11-22 23:45:40 
    a critical error in RamData.scale was resolved (values were not capped for RAMtx for querying barcodes)

    # 2022-11-24 04:45:52 
    an issue in RamData.summarize was detected, where the last record has exceptionally large values when summarizing dense matrix.
    It was due to reading the description line of the input matrix (# rows, # cols, # records) and writing it to the dense matrix.
    'create_zarr_from_mtx' method was corrected.

    # 2022-12-02 00:14:34 
    dependency on biobookshelf was dropped by migrating necessary functions to scelephant core/biobookshelf.py
    also, heavy packages (tensorflow, pynndescent, etc.) will not be loaded by default

    # 2022-12-03 11:42:43 
    an error in the RAMtx.survey_number_of_records_for_each_entry method was detected and corrected

    # 2022-12-05 13:25:20 
    support for Amazon S3 was added. currently adding ZDF metadata columns, deleting columns, updating metadata are supported and tested. supports for RamData.summarize and RamData.apply was added, too, but not yet tested.
    added methods in ZarrDataFrame to add and update 'dict_col_metadata_description' of the column metadata to annotate columns better

    # 2022-12-05 22:59:31 
    methods for file-system operations independent of the file system (local, Amazon S3 file system, or other file systems) were implemented.
    It appears Amazon S3 file system access using the S3FS package is not fork-safe. In order to access and modify files in the forked process, a FileSystemServer class was implemented. 
        For more consistent interactions and API structures, ZarrServer class was also modified so that it can perform zarr operations in either a spawned process or the current process.

    # 2022-12-07 20:22:44 
    To read and write zarr meta information in forked processes, ZarrMetadataServer was implemented.
    RamData.apply support was added to Amazon S3 file system.
    RamData.rename_layer method was added

    # 2022-12-11 17:11:25 
    RamData.summarize support was added to the Amazon S3 file system.
    a class ZarrSpinLockServer was implemented to support file-locking of ZarrDataFrame, RamData, and associated components. Methods of RamData and other objects utilizing the object ZarrSpinLockServer is being implemented.

    # 2022-12-13 03:30:26 
    A functioning version of 'create_ramtx_from_adata', 'create_ramdata_from_adata' methods were implemented, which uses multiprocessing to export count matrix to a RAMtx object. An AnnData can be exported to a RamData object using these functions.

    # 2022-12-14 01:21:04 
    the draft version of sychronization methods for ZarrDataFrame and RamData classes were implemented.
    (a commit prior to a major revision for RamData.models methods)
    
    # 2022-12-21 22:59:51 
    RamData.apply_knn method was improved by using agglomerative clustering to detect outliers during the embedding process

    # 2022-12-24 14:13:32 
    RamData.run_scanpy_using_pca method was improved by allowing parallelized run of leiden clusterings with multiple resoultion values on a single adjacency graph (shared by all the processes)
    
    # 2022-12-28 18:45:09 
    RamData.rename_model method was added (with file-locking feature)
    
    # 2022-12-29 01:16:30 
    [ZarrDataFrame] support for string data type was added for compatibility with certain annotations
    
    # 2023-01-19 00:56:42 
    [RamData] RamData.get_expr method was improved for more efficient retrieval of a filter for barcodes/features with a expression level above a threshold
    [ZarrDataFrame] resize, rechunk methods were added. The chunk size along the primary axis will be set so that the number of bytes for each chunk remain constant across the ZarrDataFrame columns.
    
    # 2023-01-20 12:55:33 
    [RAMtx] an issue in get_fork_safe_version method was resolved.
    [ZarrDataFrame] save, rechunk method multiprocessing supports were added.
    
    # 2023-01-21 15:57:18 
    improve IPython integration by enabling auto-completion of string representations of entries and column names.
    
    [RamDataLayer] improved 'select_ramtx' method to reduce file I/O by using the proprtion of active entries in each axis, not the number of active entries by themselves.
    
    # 2023-01-27 12:30:38 
    added 'flag_combine_duplicate_records' argument to 'create_zarr_from_mtx' method for de-duplication of duplicate records in the input matrix file.
    [RamDataAxis] a function for changing 'int_num_entries_in_a_chunk' of StringChunks and ZarrDataFrame metadata will be implemented to increase performance in remote access setting.
    [ZarrDataFrame] support for remote dataset will be added for the 'get_fork_safe_version' method
    
    # 2023-04-15 16:57:02 
    [RamData.identify_highly_variable_features] searching highly variable genes for each indivisual batch, and by combining "highly variable" score, identify the list of highly variable genes that are likely to represent information for each batch more accuratly.
    
    # 2023-05-06 01:12:05 
    [ZarrDataFrame] now column name with characters incompatible with the file system can be used. Internally, incompatible characters are replaced with escape characters that are compatible with file system.
    [RamData] now model name with characters incompatible with the file system is supported. Internally, incompatible characters are replaced with escape characters that are compatible with file system.
    
    # 2023-05-12 01:14:55 
    [RamData] visualization functions for categorical data were added. (RamData.get_word_count, RamData.visualize_word_count)
    
    ##### Future implementations #####
    """
]


# for creating RamData from AnnData
def create_ramtx_from_mtx(
    path_folder_mtx_10x_input: str,
    path_folder_output: str,
    mode: Literal[
        "dense", "sparse_for_querying_barcodes", "sparse_for_querying_features"
    ] = "dense",
    int_num_records_in_a_chunk: int = 10000000,
    int_buffer_size: int = 300,
    compresslevel: int = 6,
    flag_dtype_is_float: bool = False,
    int_num_threads_for_chunking: int = 5,
    int_num_threads_for_writing: int = 1,
    int_max_num_input_files_for_each_merge_sort_worker: int = 8,
    int_num_chunks_to_combine_before_concurrent_merge_sorting: int = 8,
    dtype_dense_mtx=np.uint32,
    dtype_sparse_mtx=np.float64,
    dtype_sparse_mtx_index=np.float64,
    int_num_of_records_in_a_chunk_zarr_matrix: int = 20000,
    int_num_of_entries_in_a_chunk_zarr_matrix_index: int = 1000,
    chunks_dense: tuple = (2000, 1000),
    int_num_bytes_in_a_chunk_in_a_chunk_metadata: int = 320000,
    flag_combine_duplicate_records: bool = False,
    verbose: bool = False,
    flag_debugging: bool = False,
):
    """# 2023-01-19 02:05:12
    sort a given mtx file in a very time- and memory-efficient manner, and create sparse (sorted by barcode/feature).
    when 'type' == 'dense', create a dense ramtx object in the given output folder without sorting the input mtx file in the given axis ('flag_mtx_sorted_by_id_feature')

    Arguments:
    -- basic arguments --
    'path_folder_mtx_10x_input' : a folder where mtx/feature/barcode files reside.
    'path_folder_output' : folder directory of the output folder that will contains zarr representation of a mtx file
    'mode' : {'dense' or 'sparse_for_querying_barcodes', 'sparse_for_querying_features'} : whether to create dense ramtx or sparse ramtx. for sparse ramtx, please set the appropriate 'flag_mtx_sorted_by_id_feature' flag argument for sorting. When building a dense ramtx, the chunk size can be set using 'chunks_dense' arguments
    'int_buffer_size' : the number of entries for each batch that will be given to 'pipe_sender'. increasing this number will reduce the overhead associated with interprocess-communication through pipe, but will require more memory usage
    'flag_debugging' : if True, does not delete temporary files
    flag_combine_duplicate_records : bool = False # by default, it has been set to False to increase the performance. if True, for duplicate records in the given matrix market file, values will be summed. (for example, if ( 1, 2, 10 ) and ( 1, 2, 5 ) records will be combined into ( 1, 2, 15 )).

    -- for sparse ramtx creation --
    'compresslevel' : compression level of the output Gzip file. 6 by default
    'int_max_num_input_files_for_each_merge_sort_worker' : maximum number of input pipes for each worker. this argument and the number of input pipes together will determine the number of threads used for sorting
    'flag_dtype_is_float' : set this flag to True to export float values to the output mtx matrix
    'int_num_threads_for_writing' : the number of threads for gzip writer. if 'int_num_threads' > 1, pgzip will be used to write the output gzip file. please note that pgzip (multithreaded version of gzip module) has some memory-leaking issue for large inputs.
    'int_num_records_in_a_chunk' : the number of maximum records in a chunk
    'int_num_threads_for_chunking' : number of workers for sorting and writing operations. the number of worker for reading the input gzip file will be 1.
    'dtype_sparse_mtx' (default: np.float64), dtype of the output zarr array for storing sparse matrix
    'dtype_sparse_mtx_index' (default: np.float64) : dtype of the output zarr array for storing sparse matrix indices
    'int_num_of_records_in_a_chunk_zarr_matrix' : chunk size for output zarr mtx object (sparse ramtx)
    'int_num_of_entries_in_a_chunk_zarr_matrix_index' : chunk size for output zarr mtx index object (sparse ramtx)

    -- for dense ramtx creation --
    'dtype_dense_mtx' (default: np.float64), dtype of the output zarr array for storing dense matrix
    'chunks_dense' : chunk size for dense ramtx object. if None is given, a dense ramtx object will be created. when dense ramtx object is created, the number of threads for chunking can be set using the 'int_num_threads_for_chunking' argument ( int_num_barcodes_in_a_chunk, int_num_features_in_a_chunk )

    -- for metadata creation --
    int_num_bytes_in_a_chunk_in_a_chunk_metadata : int = 320000, # the number of bytes in a chunk for metadata ZarrDataFrame objects

    """
    # check flag
    path_file_flag_completion = f"{path_folder_output}ramtx.completed.flag"
    if filesystem_operations(
        "exists", path_file_flag_completion
    ):  # exit if a flag indicating the pipeline was completed previously.
        return

    """ prepare """
    mode = mode.lower()  # handle mode argument

    # retrieve file pathes
    (
        path_file_input_bc,
        path_file_input_feature,
        path_file_input_mtx,
    ) = MTX_Get_path_essential_files(path_folder_mtx_10x_input)
    # retrieve metadata from the input mtx file
    (
        int_num_features,
        int_num_barcodes,
        int_num_records,
    ) = MTX_10X_Retrieve_number_of_rows_columns_and_records(
        path_folder_mtx_10x_input
    )  # retrieve metadata of mtx
    # create an output directory
    filesystem_operations("mkdir", path_folder_output, exist_ok=True)
    path_folder_temp = f"{path_folder_output}temp_{bk.UUID( )}/"
    filesystem_operations("mkdir", path_folder_temp, exist_ok=True)

    """
    construct RAMTx (Zarr) matrix
    """
    if mode.lower() == "dense":  # build dense ramtx based on the setting.
        create_zarr_from_mtx(
            path_file_input_mtx,
            f"{path_folder_output}matrix.zarr",
            int_buffer_size=int_buffer_size,
            chunks_dense=chunks_dense,
            dtype_mtx=dtype_dense_mtx,
            int_num_workers_for_writing_ramtx=int_num_threads_for_chunking,
            flag_combine_duplicate_records=flag_combine_duplicate_records,
        )
    else:  # build sparse ramtx
        flag_mtx_sorted_by_id_feature = (
            "feature" in mode
        )  # retrieve a flag whether to sort ramtx by id_feature or id_barcode.
        # open persistent zarr arrays to store matrix and matrix index
        za_mtx = zarr.open(
            f"{path_folder_output}matrix.zarr",
            mode="w",
            shape=(int_num_records, 2),
            chunks=(int_num_of_records_in_a_chunk_zarr_matrix, 2),
            dtype=dtype_sparse_mtx,
        )  # each mtx record will contains two values instead of three values for more compact storage
        za_mtx_index = zarr.open(
            f"{path_folder_output}matrix.index.zarr",
            mode="w",
            shape=(
                int_num_features if flag_mtx_sorted_by_id_feature else int_num_barcodes,
                2,
            ),
            chunks=(int_num_of_entries_in_a_chunk_zarr_matrix_index, 2),
            dtype=dtype_sparse_mtx_index,
        )  # max number of matrix index entries is 'int_num_records' of the input matrix. this will be resized # dtype of index should be np.float64 to be compatible with Zarr.js, since Zarr.js currently does not support np.int64...
        # build RAMtx matrix from the input matrix file
        sort_mtx(
            path_file_input_mtx,
            int_num_records_in_a_chunk=int_num_records_in_a_chunk,
            int_buffer_size=int_buffer_size,
            compresslevel=compresslevel,
            flag_dtype_is_float=flag_dtype_is_float,
            flag_mtx_sorted_by_id_feature=flag_mtx_sorted_by_id_feature,
            int_num_threads_for_chunking=int_num_threads_for_chunking,
            int_num_threads_for_writing=int_num_threads_for_writing,
            int_max_num_input_files_for_each_merge_sort_worker=int_max_num_input_files_for_each_merge_sort_worker,
            int_num_chunks_to_combine_before_concurrent_merge_sorting=int_num_chunks_to_combine_before_concurrent_merge_sorting,
            za_mtx=za_mtx,
            za_mtx_index=za_mtx_index,
        )

    """
    prepare data for the axes (features/barcodes)
    """
    """ write barcodes and features files to zarr objects"""
    for name_axis, int_num_entries in zip(
        ["barcodes", "features"], [int_num_barcodes, int_num_features]
    ):  # retrieve a flag whether the entry was used for sorting.
        # initialize the objects
        # build a ZarrDataFrame object for random access of number and categorical data of features/barcodes
        zdf = ZarrDataFrame(
            f"{path_folder_output}{name_axis}.num_and_cat.zdf",
            int_num_rows=int_num_entries,
            int_num_bytes_in_a_chunk=int_num_bytes_in_a_chunk_in_a_chunk_metadata,
            flag_store_string_as_categorical=True,
            flag_retrieve_categorical_data_as_integers=True,
            flag_enforce_name_col_with_only_valid_characters=False,
            flag_load_data_after_adding_new_column=False,
        )  # use the same chunk size for all feature/barcode objects

        # retrieve the chunk size for storing strings
        df = pd.read_csv(
            f"{path_folder_mtx_10x_input}{name_axis}.tsv.gz",
            sep="\t",
            header=None,
            nrows=100,
        )  # read the start of the data to survey the average number of strings
        l_col = list(
            f"{name_axis}_{i}" for i in range(len(df.columns))
        )  # name the columns using 0-based indices

        int_num_of_entries_in_a_chunk_metadata = zdf.get_int_num_rows_in_a_chunk(
            dtype=str,
            int_expected_length_of_string_for_string_dtype=int(
                np.ceil(np.mean(list(len(e) for e in df.values[:100, 0].ravel())))
            ),
        )

        # write zarr object for random access of string representation of features/barcodes
        za = zarr.open(
            f"{path_folder_output}{name_axis}.str.zarr",
            mode="w",
            shape=(int_num_entries, min(2, df.shape[1])),
            chunks=(int_num_of_entries_in_a_chunk_metadata, 1),
            dtype=str,
            synchronizer=zarr.ThreadSynchronizer(),
        )  # multithreading? # string object # individual columns will be chucked, so that each column can be retrieved separately.

        # create a folder to save a chunked string representations
        path_folder_str_chunks = f"{path_folder_output}{name_axis}.str.chunks/"
        filesystem_operations("mkdir", path_folder_str_chunks, exist_ok=True)
        za_str_chunks = zarr.group(path_folder_str_chunks)
        za_str_chunks.attrs["dict_metadata"] = {
            "int_num_entries": int_num_entries,
            "int_num_of_entries_in_a_chunk": int_num_of_entries_in_a_chunk_metadata,
        }  # write essential metadata for str.chunks

        # iterate over chunk by chunk
        for index_chunk, df in enumerate(
            pd.read_csv(
                f"{path_folder_mtx_10x_input}{name_axis}.tsv.gz",
                sep="\t",
                header=None,
                chunksize=int_num_of_entries_in_a_chunk_metadata,
            )
        ):  # read chunk by chunk
            values = df.values  # retrieve values

            sl_chunk = slice(
                index_chunk * int_num_of_entries_in_a_chunk_metadata,
                (index_chunk + 1) * int_num_of_entries_in_a_chunk_metadata,
            )
            values_str = values[:, :2]  # retrieve string representations
            za[sl_chunk] = values_str  # set str.zarr
            # set str.chunks
            for index_col, arr_val in enumerate(values_str.T):
                with open(
                    f"{path_folder_str_chunks}{index_chunk}.{index_col}", "wt"
                ) as newfile:  # similar organization to zarr
                    newfile.write(
                        base64_encode(gzip_bytes(("\n".join(arr_val) + "\n").encode()))
                    )
            # set num_and_cat.zdf
            if values.shape[1] > 2:
                values_num_and_cat = values[
                    :, 2:
                ]  # retrieve number and categorical data
                for arr_val, name_col in zip(values[:, 2:].T, l_col[2:]):
                    zdf[name_col, sl_chunk] = arr_val

    """ write metadata """
    # compose metadata
    dict_metadata = {
        "path_folder_mtx_10x_input": path_folder_mtx_10x_input,
        "mode": mode,
        "str_completed_time": bk.TIME_GET_timestamp(True),
        "int_num_features": int_num_features,
        "int_num_barcodes": int_num_barcodes,
        "int_num_records": int_num_records,
        "version": _version_,
    }
    if mode.lower() != "dense":
        dict_metadata["flag_ramtx_sorted_by_id_feature"] = flag_mtx_sorted_by_id_feature
    root = zarr.group(f"{path_folder_output}")
    root.attrs["dict_metadata"] = dict_metadata

    # delete temp folder
    filesystem_operations("rm", path_folder_temp)

    """ write a flag indicating the export has been completed """
    with open(path_file_flag_completion, "w") as file:
        file.write(bk.TIME_GET_timestamp(True))


def create_ramdata_from_mtx(
    path_folder_mtx_10x_input: str,
    path_folder_ramdata_output: str,
    set_modes: set = {"dense"},
    name_layer: str = "raw",
    int_num_records_in_a_chunk: int = 10000000,
    int_buffer_size: int = 300,
    compresslevel: int = 6,
    flag_dtype_is_float: bool = False,
    int_num_threads_for_chunking: int = 5,
    int_num_threads_for_writing: int = 1,
    int_max_num_input_files_for_each_merge_sort_worker: int = 8,
    int_num_chunks_to_combine_before_concurrent_merge_sorting: int = 8,
    dtype_dense_mtx=np.uint32,
    dtype_sparse_mtx=np.float64,
    dtype_sparse_mtx_index=np.float64,
    int_num_of_records_in_a_chunk_zarr_matrix: int = 20000,
    int_num_of_entries_in_a_chunk_zarr_matrix_index: int = 1000,
    chunks_dense: tuple = (2000, 1000),
    int_num_bytes_in_a_chunk_in_a_chunk_metadata: int = 320000,
    flag_combine_duplicate_records: bool = False,
    flag_multiprocessing: bool = True,
    verbose: bool = False,
    flag_debugging: bool = False,
):
    """# 2022-12-13 22:25:38
    sort a given mtx file in a very time- and memory-efficient manner, and create sparse (sorted by barcode/feature).
    when 'type' == 'dense', create a dense ramtx object in the given output folder without sorting the input mtx file in the given axis ('flag_mtx_sorted_by_id_feature')

    Arguments:
    -- basic arguments --
    'path_folder_mtx_10x_input' : a folder where mtx/feature/barcode files reside.
    'path_folder_ramdata_output' : an output folder directory of the RamData object
    'set_modes' : a set of {'dense', 'sparse_for_querying_barcodes', 'sparse_for_querying_features'} : modes of ramtxs to build.
                'dense' : dense ramtx. When building a dense ramtx, the chunk size can be set using 'chunks_dense' arguments
                'sparse_for_querying_barcodes/features' : sparse ramtx sorted by each axis
    'int_buffer_size' : the number of entries for each batch that will be given to 'pipe_sender'. increasing this number will reduce the overhead associated with interprocess-communication through pipe, but will require more memory usage
    'flag_debugging' : if True, does not delete temporary files
    flag_combine_duplicate_records : bool = False # by default, it has been set to False to increase the performance. if True, for duplicate records in the given matrix market file, values will be summed. (for example, if ( 1, 2, 10 ) and ( 1, 2, 5 ) records will be combined into ( 1, 2, 15 )).

    -- for sparse ramtx creation --
    'compresslevel' : compression level of the output Gzip file. 6 by default
    'int_max_num_input_files_for_each_merge_sort_worker' : maximum number of input pipes for each worker for concurrent-merge-sorting. this argument and the number of input pipes together will determine the number of threads used for sorting.
    'flag_dtype_is_float' : set this flag to True to export float values to the output mtx matrix
    'int_num_threads_for_writing' : the number of threads for gzip writer. if 'int_num_threads' > 1, pgzip will be used to write the output gzip file. please note that pgzip (multithreaded version of gzip module) has some memory-leaking issue for large inputs.
    'int_num_records_in_a_chunk' : the number of maximum records in a chunk
    'int_num_threads_for_chunking' : number of workers for sorting and writing operations. the number of worker for reading the input gzip file will be 1.
    'int_num_chunks_to_combine_before_concurrent_merge_sorting' : preliminary merge-sorting step. in a typical system, a single process can open upto ~1000 files at once. therefore, merge-sorting more than 1000 files cannot be done in a single concurrent merge-sort step. therefore, sorted chunks will be combined into a larger chunk before they can be merge-sorted into a single output file.
            for very large single-cell data (>10 million single-cells or > 50 GB of matrix), increase the number given through this argument to avoid too-many-files-opened error.
    'dtype_sparse_mtx' (default: np.float64), dtype of the output zarr array for storing sparse matrix
    'dtype_sparse_mtx_index' (default: np.float64) : dtype of the output zarr array for storing sparse matrix indices
    'int_num_of_records_in_a_chunk_zarr_matrix' : chunk size for output zarr mtx object (sparse ramtx)
    'int_num_of_entries_in_a_chunk_zarr_matrix_index' : chunk size for output zarr mtx index object (sparse ramtx)

    -- for dense ramtx creation --
    'dtype_dense_mtx' (default: np.float64), dtype of the output zarr array for storing dense matrix
    'chunks_dense' : chunk size for dense ramtx object. if None is given, a dense ramtx object will be created. when dense ramtx object is created, the number of threads for chunking can be set using the 'int_num_threads_for_chunking' argument ( int_num_barcodes_in_a_chunk, int_num_features_in_a_chunk )

    -- for metadata creation --
    int_num_bytes_in_a_chunk_in_a_chunk_metadata : int = 320000, # the number of bytes in a chunk for metadata ZarrDataFrame objects

    -- for RamData creation --
    'name_layer' : a name of the ramdata layer to create (default: raw)
    """
    """ handle arguments """
    set_valid_modes = {
        "dense",
        "sparse_for_querying_barcodes",
        "sparse_for_querying_features",
    }
    set_modes = set(
        e for e in set(e.lower().strip() for e in set_modes) if e in set_valid_modes
    )  # retrieve valid mode
    assert len(set_modes) > 0  # at least one valid mode should exists

    # build RAMtx objects
    path_folder_ramdata_layer = f"{path_folder_ramdata_output}{name_layer}/"  # define directory of the output data layer

    # define keyword arguments for ramtx building
    kwargs_ramtx = {
        "int_num_records_in_a_chunk": int_num_records_in_a_chunk,
        "int_buffer_size": int_buffer_size,
        "compresslevel": compresslevel,
        "flag_dtype_is_float": flag_dtype_is_float,
        "int_num_threads_for_chunking": int_num_threads_for_chunking,
        "int_num_threads_for_writing": int_num_threads_for_writing,
        "int_max_num_input_files_for_each_merge_sort_worker": int_max_num_input_files_for_each_merge_sort_worker,
        "int_num_chunks_to_combine_before_concurrent_merge_sorting": int_num_chunks_to_combine_before_concurrent_merge_sorting,
        "dtype_dense_mtx": dtype_dense_mtx,
        "dtype_sparse_mtx": dtype_sparse_mtx,
        "dtype_sparse_mtx_index": dtype_sparse_mtx_index,
        "int_num_of_records_in_a_chunk_zarr_matrix": int_num_of_records_in_a_chunk_zarr_matrix,
        "int_num_of_entries_in_a_chunk_zarr_matrix_index": int_num_of_entries_in_a_chunk_zarr_matrix_index,
        "chunks_dense": chunks_dense,
        "int_num_bytes_in_a_chunk_in_a_chunk_metadata": int_num_bytes_in_a_chunk_in_a_chunk_metadata,
        "flag_combine_duplicate_records": flag_combine_duplicate_records,
        "verbose": verbose,
        "flag_debugging": flag_debugging,
    }

    # compose processes
    l_p = []
    for mode in set_modes:
        l_p.append(
            mp.Process(
                target=create_ramtx_from_mtx,
                args=(
                    path_folder_mtx_10x_input,
                    f"{path_folder_ramdata_layer}{mode}/",
                    mode,
                ),
                kwargs=kwargs_ramtx,
            )
        )
    # run processes
    for p in l_p:
        p.start()
    for p in l_p:
        p.join()

    # copy features/barcode.tsv.gz random access files for the web (stacked base64 encoded tsv.gz files)
    # copy features/barcode string representation zarr objects
    # copy features/barcode ZarrDataFrame containing number/categorical data
    for name_axis in ["features", "barcodes"]:
        for str_suffix in [".str.chunks", ".str.zarr", ".num_and_cat.zdf"]:
            bk.OS_Run(
                [
                    "cp",
                    "-r",
                    f"{path_folder_ramdata_layer}{mode}/{name_axis}{str_suffix}",
                    f"{path_folder_ramdata_output}{name_axis}{str_suffix}",
                ]
            )

    # write ramdata metadata
    (
        int_num_features,
        int_num_barcodes,
        int_num_records,
    ) = MTX_10X_Retrieve_number_of_rows_columns_and_records(
        path_folder_mtx_10x_input
    )  # retrieve metadata of the input 10X mtx
    root = zarr.group(path_folder_ramdata_output)
    root.attrs["dict_metadata"] = {
        "path_folder_mtx_10x_input": path_folder_mtx_10x_input,
        "str_completed_time": bk.TIME_GET_timestamp(True),
        "int_num_features": int_num_features,
        "int_num_barcodes": int_num_barcodes,
        "layers": {name_layer: dict()},
        "identifier": bk.UUID(),
        "models": dict(),
        "version": _version_,
    }
    # write layer metadata
    lay = zarr.group(path_folder_ramdata_layer)
    lay.attrs["dict_metadata"] = {
        "set_modes": list(set_modes)
        + (
            ["dense_for_querying_barcodes", "dense_for_querying_features"]
            if "dense" in set_modes
            else []
        ),  # dense ramtx can be operated for querying either barcodes/features
        "version": _version_,
    }


def create_ramtx_from_adata(
    adata,
    path_folder_output: str,
    mode: Literal[
        "dense", "sparse_for_querying_features", "sparse_for_querying_barcodes"
    ] = "sparse_for_querying_features",
    int_num_threads_for_writing_matrix: int = 5,
    dtype_dense_mtx=np.float64,
    dtype_sparse_mtx=np.float64,
    dtype_sparse_mtx_index=np.float64,
    int_num_of_records_in_a_chunk_zarr_matrix: int = 20000,
    int_num_of_entries_in_a_chunk_zarr_matrix_index: int = 1000,
    int_num_of_entries_in_a_batch_for_writing_sparse_matrix: int = 350,
    float_ratio_padding_for_zarr_sparse_matrix_output: float = 0.5,
    chunks_dense: tuple = (2000, 1000),
    int_num_bytes_in_a_chunk_in_a_chunk_metadata: int = 320000,
    int_max_num_categories_in_metadata: int = 10000,
    dict_kw_zdf: dict = {
        "flag_store_string_as_categorical": True,
        "flag_load_data_after_adding_new_column": False,
        "flag_store_64bit_integer_as_float": True,
    },
    l_name_col_str_repr_bc: list = ["index"],
    l_name_col_str_repr_ft: list = ["index", "index"],
    verbose: bool = False,
    flag_debugging: bool = False,
):
    """# 2023-03-07 22:13:52
    Write a given AnnData object as a RAMtx object

    Arguments:
    -- basic arguments --
    'adata' : an AnnData object to write as a RAMtx object
    'path_folder_output' : folder directory of the output folder that will contains zarr representation of the AnnData object
    'mode' : {'dense' or 'sparse_for_querying_barcodes', 'sparse_for_querying_features'} : whether to create dense ramtx or sparse ramtx. When building a dense ramtx, the chunk size can be set using 'chunks_dense' arguments
    'flag_debugging' : if True, does not delete temporary files

    -- for sparse ramtx --
    int_num_threads_for_writing_matrix = 5 # the number of processes for writing a zarr matrix

    'dtype_sparse_mtx' (default: np.float64), dtype of the output zarr array for storing sparse matrix
    'dtype_sparse_mtx_index' (default: np.float64) : dtype of the output zarr array for storing sparse matrix indices
    'int_num_of_records_in_a_chunk_zarr_matrix' : chunk size for output zarr mtx object (sparse ramtx)
    'int_num_of_entries_in_a_chunk_zarr_matrix_index' : chunk size for output zarr mtx index object (sparse ramtx)
    int_num_of_entries_in_a_batch_for_writing_sparse_matrix : int = 350 # the number of entries in a batch for writing a sparse matrix
    float_ratio_padding_for_zarr_sparse_matrix_output : float = 0.5 # the ratio of the padding relative to the length of the sparse matrix for padding to accomodate fragmentations from multi-processing.

    -- for dense ramtx --
    'dtype_dense_mtx' (default: np.float64), dtype of the output zarr array for storing dense matrix
    'chunks_dense' : chunk size for dense ramtx object. if None is given, a dense ramtx object will be created. when dense ramtx object is created, the number of threads for chunking can be set using the 'int_num_threads_for_chunking' argument ( int_num_barcodes_in_a_chunk, int_num_features_in_a_chunk )

    -- for metadata --
    int_num_bytes_in_a_chunk_in_a_chunk_metadata : int = 320000, # the number of bytes in a chunk for metadata ZarrDataFrame objects
    int_max_num_categories_in_metadata : int = 10000 # ignore columns with more than 'int_max_num_categories_in_metadata' number of categories.
    dict_kw_zdf : dict = dict( ) # keyworded arguments for the initialization of the ZarrDataFrame
    l_name_col_str_repr_bc : list = [ 'index' ] # the list of name of columns for string representations of the barcode axis. 'index' for using index values for string representations.
    l_name_col_str_repr_ft : list = [ 'index', 'index' ] # the list of name of columns for string representations of the feature axis. 'index' for using index values for string representations.
    """
    # check flag
    path_file_flag_completion = f"{path_folder_output}ramtx.completed.flag"
    if filesystem_operations(
        "exists", path_file_flag_completion
    ):  # exit if a flag indicating the pipeline was completed previously.
        return

    """ prepare """
    mode = mode.lower()  # handle mode argument

    # retrieve metadata from the input mtx file
    int_num_features, int_num_barcodes, int_num_records = (
        len(adata.var),
        len(adata.obs),
        adata.X.count_nonzero(),
    )  # retrieve metadata of mtx
    # create an output directory
    filesystem_operations("mkdir", path_folder_output, exist_ok=True)
    path_folder_temp = f"{path_folder_output}temp_{bk.UUID( )}/"
    filesystem_operations("mkdir", path_folder_temp, exist_ok=True)

    """
    construct RAMTx (Zarr) matrix
    """
    pbar = progress_bar(
        desc=f"RAMtx ({mode})", total=int_num_records
    )  # set up the progress bar

    if mode == "dense":  # build a dense ramtx based on the setting.
        # open a persistent zarr array
        za_mtx = zarr.open(
            f"{path_folder_output}matrix.zarr",
            mode="w",
            shape=(int_num_barcodes, int_num_features),
            chunks=chunks_dense,
            dtype=dtype_sparse_mtx,
        )  # each mtx record will contains two values instead of three values for more compact storage

        def __parse_adata(l_pipe_sender):
            """# 2022-12-12 17:34:39
            parse input adata along the chunk boundary and send parsed result to workers writing the dense matrix
            """
            int_num_workers = len(l_pipe_sender)
            int_pos = 0
            X = adata.X
            int_index_worker = 0
            while int_pos < int_num_barcodes:
                # retrieve data for the current chunks
                sl = slice(int_pos, min(int_pos + chunks_dense[0], int_num_barcodes))
                arr_int_bc, arr_int_ft, arr_value = scipy.sparse.find(X[sl])
                arr_int_bc += int_pos  # add the offset
                l_pipe_sender[int_index_worker].send(
                    (arr_int_bc, arr_int_ft, arr_value)
                )
                # prepare next chunks
                int_index_worker = (int_index_worker + 1) % int_num_workers
                int_pos += chunks_dense[0]
            # notify workers that all works have been distributed
            for pipe_sender in l_pipe_sender:
                pipe_sender.send(None)

        def __write_mtx(pipe_receiver, pipe_sender):
            """# 2022-12-12 15:15:40
            write a dense mtx
            """
            while True:
                ins = pipe_receiver.recv()
                if ins is None:
                    break
                arr_int_bc, arr_int_ft, arr_value = ins  # parse the input
                za_mtx.set_coordinate_selection((arr_int_bc, arr_int_ft), arr_value)
                pipe_sender.send(len(arr_value))  # report the number of records written
            pipe_sender.send(None)  # report that all works have been completed

    elif "sparse" in mode:  # build a sparse ramtx based on the setting.
        flag_mtx_sorted_by_id_feature = (
            "feature" in mode
        )  # retrieve a flag whether to sort ramtx by id_feature or id_barcode.

        # open persistent zarr arrays to store matrix and matrix index
        za_mtx = zarr.open(
            f"{path_folder_output}matrix.zarr",
            mode="w",
            shape=(
                int(
                    int_num_records
                    * (1 + float_ratio_padding_for_zarr_sparse_matrix_output)
                ),
                2,
            ),
            chunks=(int_num_of_records_in_a_chunk_zarr_matrix, 2),
            dtype=dtype_sparse_mtx,
        )  # each mtx record will contains two values instead of three values for more compact storage # initialize the matrix with a sufficiently large padding
        za_mtx_index = zarr.open(
            f"{path_folder_output}matrix.index.zarr",
            mode="w",
            shape=(
                int_num_features if flag_mtx_sorted_by_id_feature else int_num_barcodes,
                2,
            ),
            chunks=(int_num_of_entries_in_a_chunk_zarr_matrix_index, 2),
            dtype=dtype_sparse_mtx_index,
        )  # max number of matrix index entries is 'int_num_records' of the input matrix. this will be resized # dtype of index should be np.float64 to be compatible with Zarr.js, since Zarr.js currently does not support np.int64...

        def __parse_adata(l_pipe_sender):
            """# 2022-12-12 17:34:39
            parse input adata along the chunk boundary and send parsed result to workers writing the dense matrix
            """
            # prepare
            int_num_workers = len(l_pipe_sender)
            int_pos = 0
            X = adata.X
            int_index_worker = 0
            int_index_chunk_of_mtx_index = 0
            int_index_chunk_of_mtx = 0
            int_num_entries_in_the_axis_for_querying = (
                int_num_features if flag_mtx_sorted_by_id_feature else int_num_barcodes
            )

            while int_pos < int_num_entries_in_the_axis_for_querying:
                # retrieve data for the current chunks
                int_pos_end = min(
                    int_pos + int_num_of_entries_in_a_batch_for_writing_sparse_matrix,
                    (int_index_chunk_of_mtx_index + 1)
                    * int_num_of_entries_in_a_chunk_zarr_matrix_index,
                )  # the position of the end of the chunks that will be processed in the current batch
                sl = slice(int_pos, int_pos_end)
                arr_int_bc, arr_int_ft, arr_value = scipy.sparse.find(
                    X[:, sl] if flag_mtx_sorted_by_id_feature else X[sl]
                )
                (
                    arr_int_entry_of_the_axis_for_querying,
                    arr_int_entry_of_the_axis_not_for_querying,
                ) = (
                    (arr_int_ft, arr_int_bc)
                    if flag_mtx_sorted_by_id_feature
                    else (arr_int_bc, arr_int_ft)
                )
                arr_int_entry_of_the_axis_for_querying += int_pos  # add the offset
                int_num_records = len(arr_value)

                # send parsed data to the worker process
                l_pipe_sender[int_index_worker].send(
                    (
                        int_pos,
                        int_pos_end,
                        int_index_chunk_of_mtx,
                        arr_int_entry_of_the_axis_for_querying,
                        arr_int_entry_of_the_axis_not_for_querying,
                        arr_value,
                    )
                )

                # prepare next chunks
                int_pos = int_pos_end  # update 'int_pos'
                if (
                    int_pos % int_num_of_entries_in_a_chunk_zarr_matrix_index
                    > int_index_chunk_of_mtx_index
                ):  # if the updated position mapped to the different chunks from the previous chunks
                    int_index_worker = (
                        int_index_worker + 1
                    ) % int_num_workers  # change worker process
                    int_index_chunk_of_mtx_index = (
                        int_pos % int_num_of_entries_in_a_chunk_zarr_matrix_index
                    )  # update 'int_index_chunk_of_mtx_index'
                int_index_chunk_of_mtx += int(
                    np.ceil(int_num_records / int_num_of_records_in_a_chunk_zarr_matrix)
                )  # update 'int_index_chunk_of_mtx'

            # notify workers that all works have been distributed
            for pipe_sender in l_pipe_sender:
                pipe_sender.send(None)

        def __write_mtx(pipe_receiver, pipe_sender):
            """# 2022-12-12 15:15:40
            write a dense mtx
            """
            while True:
                ins = pipe_receiver.recv()
                if ins is None:
                    break
                (
                    int_pos,
                    int_pos_end,
                    int_index_chunk_of_mtx,
                    arr_int_entry_of_the_axis_for_querying,
                    arr_int_entry_of_the_axis_not_for_querying,
                    arr_value,
                ) = ins  # parse the input

                arr_argsort = (
                    arr_int_entry_of_the_axis_for_querying.argsort()
                )  # retrieve an argsort array
                # sort records
                arr_int_entry_of_the_axis_for_querying = (
                    arr_int_entry_of_the_axis_for_querying[arr_argsort]
                )
                arr_int_entry_of_the_axis_not_for_querying = (
                    arr_int_entry_of_the_axis_not_for_querying[arr_argsort]
                )
                arr_value = arr_value[arr_argsort]
                # retrieve the number of records
                int_num_records = len(arr_value)

                # retrieve boundaries of the sorted entries
                l_boundary = (
                    [0]
                    + list(
                        np.where(np.diff(arr_int_entry_of_the_axis_for_querying))[0] + 1
                    )
                    + [int_num_records]
                )
                arr_index = np.array(
                    [l_boundary[:-1], l_boundary[1:]]
                ).T  # compose the array of indices based on the locations of the boundaries

                # export the sparse matrix
                st, en = (
                    int_index_chunk_of_mtx * int_num_of_records_in_a_chunk_zarr_matrix,
                    int_index_chunk_of_mtx * int_num_of_records_in_a_chunk_zarr_matrix
                    + int_num_records,
                )
                arr_index += st  # add the offset from the start of the sparse matrix to the index coordinates
                za_mtx.set_orthogonal_selection(
                    slice(st, en),
                    np.vstack(
                        (arr_int_entry_of_the_axis_not_for_querying, arr_value)
                    ).T,
                )
                za_mtx_index.set_orthogonal_selection(
                    sorted(set(arr_int_entry_of_the_axis_for_querying)), arr_index
                )

                pipe_sender.send(
                    int_num_records
                )  # report the number of records written
            pipe_sender.send(None)  # report that all works have been completed

    # compose pipes and processes
    l_pipe_ins = list(mp.Pipe() for i in range(int_num_threads_for_writing_matrix))
    l_pipe_outs = list(mp.Pipe() for i in range(int_num_threads_for_writing_matrix))
    l_pipe_receiver = list(
        l_pipe_outs[i][1] for i in range(int_num_threads_for_writing_matrix)
    )
    l_p = list(
        mp.Process(target=__write_mtx, args=(l_pipe_ins[i][1], l_pipe_outs[i][0]))
        for i in range(int_num_threads_for_writing_matrix)
    )
    l_p.append(
        mp.Process(
            target=__parse_adata,
            args=(
                list(
                    l_pipe_ins[i][0] for i in range(int_num_threads_for_writing_matrix)
                ),
            ),
        )
    )

    # start the processes
    for p in l_p:
        p.start()

    # monitor the progress
    arr_flag_work_remaining = np.ones(
        int_num_threads_for_writing_matrix
    )  # a list of flag indicating works are remaining
    int_index_worker = 0
    while arr_flag_work_remaining.sum() > 0:  # until all workers completed the works
        if (
            arr_flag_work_remaining[int_index_worker] > 0
        ):  # if the current process is working
            if l_pipe_receiver[int_index_worker].poll():
                outs = l_pipe_receiver[int_index_worker].recv()
                if outs is None:
                    arr_flag_work_remaining[int_index_worker] = 0
                else:
                    int_num_processed_records = outs  # parse the output
                    pbar.update(int_num_processed_records)  # update the progress bar
        int_index_worker = (int_index_worker + 1) % int_num_threads_for_writing_matrix

    # join the processes
    for p in l_p:
        p.join()
    pbar.close()  # close the progress bar

    """
    prepare data for the axes (features/barcodes)
    """
    """ write barcodes and features files to zarr objects"""
    for name_axis, int_num_entries, df, m, l_name_col_str_repr in zip(
        ["barcodes", "features"],
        [int_num_barcodes, int_num_features],
        [adata.obs, adata.var],
        [adata.obsm, adata.varm],
        [l_name_col_str_repr_bc, l_name_col_str_repr_ft],
    ):
        # initialize a ZarrDataFrame object for random access of number and categorical data of features/barcodes
        zdf = ZarrDataFrame(
            f"{path_folder_output}{name_axis}.num_and_cat.zdf",
            int_num_rows=int_num_entries,
            int_num_bytes_in_a_chunk=int_num_bytes_in_a_chunk_in_a_chunk_metadata,
            **dict_kw_zdf,
        )  # use the same chunk size for feature/barcode objects

        # retrieve string representations
        l_l_str = []
        for name_col_str_repr in l_name_col_str_repr:
            l_l_str.append(
                df.index.values
                if name_col_str_repr == "index"
                else df[name_col_str_repr].values
            )  # collect string representations
        arr_str = np.vstack(l_l_str).T  #  compose 'arr_str'
        int_num_str_repr = len(l_name_col_str_repr)  # retrieve 'int_num_str_repr'
        del l_l_str

        # retrieve the chunk size for storing strings
        int_num_of_entries_in_a_chunk_metadata = zdf.get_int_num_rows_in_a_chunk(
            dtype=str,
            int_expected_length_of_string_for_string_dtype=int(
                np.ceil(np.mean(list(len(e) for e in arr_str[:10].ravel())))
            ),
        )

        # initialize a zarr object for writing string values for random access of string representation of features/barcodes
        za = zarr.open(
            f"{path_folder_output}{name_axis}.str.zarr",
            mode="w",
            shape=(int_num_entries, int_num_str_repr),
            chunks=(int_num_of_entries_in_a_chunk_metadata, 1),
            dtype=str,
        )  # string object # individual columns will be chucked, so that each column can be retrieved separately.

        # rename columns with invalid characters
        df.columns = list(col.replace("/", "__") for col in df.columns.values)

        # drop the columns with too many categories (these columns are likely to contain identifiers)
        df = df[
            list(
                col
                for col in df.columns.values
                if len(df[col].unique()) <= int_max_num_categories_in_metadata
            )
        ]

        df.reset_index(drop=True, inplace=True)  # reset the index
        zdf.update(df)  # save the metadata

        # create a folder to save a chunked string representations
        path_folder_str_chunks = f"{path_folder_output}{name_axis}.str.chunks/"
        filesystem_operations("mkdir", path_folder_str_chunks, exist_ok=True)
        za_str_chunks = zarr.group(path_folder_str_chunks)
        za_str_chunks.attrs["dict_metadata"] = {
            "int_num_entries": int_num_entries,
            "int_num_of_entries_in_a_chunk": int_num_of_entries_in_a_chunk_metadata,
        }  # write essential metadata for str.chunks

        # add multi-dimensional data to the metadata
        for name_key in m:
            zdf[name_key] = m[name_key]

        # save string representations
        za[:] = arr_str  # set str.zarr
        # save str.chunks
        index_chunk = 0
        while index_chunk * int_num_of_entries_in_a_chunk_metadata < int_num_entries:
            for index_col, arr_val in enumerate(
                arr_str[
                    index_chunk
                    * int_num_of_entries_in_a_chunk_metadata : (index_chunk + 1)
                    * int_num_of_entries_in_a_chunk_metadata
                ].T
            ):
                with open(
                    f"{path_folder_str_chunks}{index_chunk}.{index_col}", "wt"
                ) as newfile:  # similar organization to zarr
                    newfile.write(
                        base64_encode(gzip_bytes(("\n".join(arr_val) + "\n").encode()))
                    )
            index_chunk += 1  # update 'index_chunk'

    """ write metadata """
    # compose metadata
    dict_metadata = {
        "path_folder_mtx_10x_input": None,
        "mode": mode,
        "str_completed_time": bk.TIME_GET_timestamp(True),
        "int_num_features": int_num_features,
        "int_num_barcodes": int_num_barcodes,
        "int_num_records": int_num_records,
        "version": _version_,
    }
    if mode.lower() != "dense":
        dict_metadata["flag_ramtx_sorted_by_id_feature"] = flag_mtx_sorted_by_id_feature
    root = zarr.group(f"{path_folder_output}")
    root.attrs["dict_metadata"] = dict_metadata

    # delete temp folder
    filesystem_operations("rm", path_folder_temp)

    """ write a flag indicating the export has been completed """
    with open(path_file_flag_completion, "w") as file:
        file.write(bk.TIME_GET_timestamp(True))
    logger.info(f"Exporting of a RAMtx object at '{path_folder_output}' was completed")


def create_ramdata_from_adata(
    adata,
    path_folder_ramdata_output: str,
    set_modes: set = {"sparse_for_querying_features"},
    name_layer: str = "normalized_log1p_scaled",
    int_num_threads_for_writing_matrix: int = 5,
    dtype_dense_mtx=np.float64,
    dtype_sparse_mtx=np.float64,
    dtype_sparse_mtx_index=np.float64,
    int_num_of_records_in_a_chunk_zarr_matrix: int = 20000,
    int_num_of_entries_in_a_chunk_zarr_matrix_index: int = 1000,
    int_num_of_entries_in_a_batch_for_writing_sparse_matrix: int = 350,
    float_ratio_padding_for_zarr_sparse_matrix_output: float = 0.5,
    chunks_dense: tuple = (2000, 1000),
    int_num_bytes_in_a_chunk_in_a_chunk_metadata: int = 320000,
    int_max_num_categories_in_metadata: int = 10000,
    dict_kw_zdf: dict = {
        "flag_store_string_as_categorical": True,
        "flag_load_data_after_adding_new_column": False,
        "flag_store_64bit_integer_as_float": True,
    },
    l_name_col_str_repr_bc: list = ["index"],
    l_name_col_str_repr_ft: list = ["index", "index"],
    flag_multiprocessing: bool = True,
    verbose: bool = False,
    flag_debugging: bool = False,
):
    """# 2023-03-07 22:13:58
    Write a given AnnData object as a RamData object

    Arguments:
    -- basic arguments --
    'adata' : an AnnData object to write as a RamData object
    'path_folder_ramdata_output' : an output folder directory of the RamData object
    'set_modes' : a set of {'dense', 'sparse_for_querying_barcodes', 'sparse_for_querying_features'} : modes of ramtxs to build.
                'dense' : dense ramtx. When building a dense ramtx, the chunk size can be set using 'chunks_dense' arguments
                'sparse_for_querying_barcodes/features' : sparse ramtx sorted by each axis
    'flag_debugging' : if True, does not delete temporary files

    -- for sparse ramtx --
    int_num_threads_for_writing_matrix : int = 5 # the number of processes for writing a zarr matrix

    'dtype_sparse_mtx' (default: np.float64), dtype of the output zarr array for storing sparse matrix
    'dtype_sparse_mtx_index' (default: np.float64) : dtype of the output zarr array for storing sparse matrix indices
    'int_num_of_records_in_a_chunk_zarr_matrix' : chunk size for output zarr mtx object (sparse ramtx)
    'int_num_of_entries_in_a_chunk_zarr_matrix_index' : chunk size for output zarr mtx index object (sparse ramtx)
    int_num_of_entries_in_a_batch_for_writing_sparse_matrix : int = 350 # the number of entries in a batch for writing a sparse matrix
    float_ratio_padding_for_zarr_sparse_matrix_output : float = 0.5 # the ratio of the padding relative to the length of the sparse matrix for padding to accomodate fragmentations from multi-processing.

    -- for dense ramtx --
    'dtype_dense_mtx' (default: np.float64), dtype of the output zarr array for storing dense matrix
    'chunks_dense' : chunk size for dense ramtx object. if None is given, a dense ramtx object will be created. when dense ramtx object is created, the number of threads for chunking can be set using the 'int_num_threads_for_chunking' argument ( int_num_barcodes_in_a_chunk, int_num_features_in_a_chunk )

    -- for metadata --
    int_num_bytes_in_a_chunk_in_a_chunk_metadata : int = 320000, # the number of bytes in a chunk for metadata ZarrDataFrame objects
    int_max_num_categories_in_metadata : int = 10000 # ignore columns with more than 'int_max_num_categories_in_metadata' number of categories.
    dict_kw_zdf : dict = dict( ) # keyworded arguments for the initialization of the ZarrDataFrame
    l_name_col_str_repr_bc : list = [ 'index' ] # the list of name of columns for string representations of the barcode axis. 'index' for using index values for string representations.
    l_name_col_str_repr_ft : list = [ 'index', 'index' ] # the list of name of columns for string representations of the feature axis. 'index' for using index values for string representations.

    -- for RamData creation --
    name_layer : str : a name of the ramdata layer to create (default: raw)
    flag_multiprocessing : bool = True # if True, create RAMtx objects in parallel
    """
    """ handle arguments """
    set_valid_modes = {
        "dense",
        "sparse_for_querying_barcodes",
        "sparse_for_querying_features",
    }
    set_modes = set(
        e for e in set(e.lower().strip() for e in set_modes) if e in set_valid_modes
    )  # retrieve valid mode
    if len(set_modes) == 0:  # at least one valid mode should exists
        return  # exit early

    # build RAMtx objects
    path_folder_ramdata_layer = f"{path_folder_ramdata_output}{name_layer}/"  # define directory of the output data layer

    # define keyword arguments for ramtx building
    kwargs_ramtx = {
        "int_num_threads_for_writing_matrix": int_num_threads_for_writing_matrix,
        "dtype_dense_mtx": dtype_dense_mtx,
        "dtype_sparse_mtx": dtype_sparse_mtx,
        "dtype_sparse_mtx_index": dtype_sparse_mtx_index,
        "int_num_of_records_in_a_chunk_zarr_matrix": int_num_of_records_in_a_chunk_zarr_matrix,
        "int_num_of_entries_in_a_chunk_zarr_matrix_index": int_num_of_entries_in_a_chunk_zarr_matrix_index,
        "int_num_of_entries_in_a_batch_for_writing_sparse_matrix": int_num_of_entries_in_a_batch_for_writing_sparse_matrix,
        "float_ratio_padding_for_zarr_sparse_matrix_output": float_ratio_padding_for_zarr_sparse_matrix_output,
        "chunks_dense": chunks_dense,
        "int_num_bytes_in_a_chunk_in_a_chunk_metadata": int_num_bytes_in_a_chunk_in_a_chunk_metadata,
        "int_max_num_categories_in_metadata": int_max_num_categories_in_metadata,
        "dict_kw_zdf": dict_kw_zdf,
        "l_name_col_str_repr_bc": l_name_col_str_repr_bc,
        "l_name_col_str_repr_ft": l_name_col_str_repr_ft,
        "verbose": verbose,
        "flag_debugging": flag_debugging,
    }

    if flag_multiprocessing:  # build multiple RAMtx objects simultaneously
        # compose processes
        l_p = []
        for mode in set_modes:
            l_p.append(
                mp.Process(
                    target=create_ramtx_from_adata,
                    args=(adata, f"{path_folder_ramdata_layer}{mode}/", mode),
                    kwargs=kwargs_ramtx,
                )
            )
        # run processes
        for p in l_p:
            p.start()
        for p in l_p:
            p.join()
    else:
        # build each RAMtx one at a time
        for mode in set_modes:
            create_ramtx_from_adata(
                adata, f"{path_folder_ramdata_layer}{mode}/", mode, **kwargs_ramtx
            )

    # copy features/barcode.tsv.gz random access files for the web (stacked base64 encoded tsv.gz files)
    # copy features/barcode string representation zarr objects
    # copy features/barcode ZarrDataFrame containing number/categorical data
    for name_axis in ["features", "barcodes"]:
        for str_suffix in [".str.chunks", ".str.zarr", ".num_and_cat.zdf"]:
            bk.OS_Run(
                [
                    "cp",
                    "-r",
                    f"{path_folder_ramdata_layer}{mode}/{name_axis}{str_suffix}",
                    f"{path_folder_ramdata_output}{name_axis}{str_suffix}",
                ]
            )

    # write ramdata metadata
    int_num_features, int_num_barcodes, int_num_records = (
        len(adata.var),
        len(adata.obs),
        adata.X.count_nonzero(),
    )  # retrieve metadata of mtx
    root = zarr.group(path_folder_ramdata_output)
    root.attrs["dict_metadata"] = {
        "path_folder_mtx_10x_input": None,
        "str_completed_time": bk.TIME_GET_timestamp(True),
        "int_num_features": int_num_features,
        "int_num_barcodes": int_num_barcodes,
        "layers": {name_layer: dict()},
        "identifier": bk.UUID(),
        "models": dict(),
        "version": _version_,
    }
    # write layer metadata
    lay = zarr.group(path_folder_ramdata_layer)
    lay.attrs["dict_metadata"] = {
        "set_modes": list(set_modes)
        + (
            ["dense_for_querying_barcodes", "dense_for_querying_features"]
            if "dense" in set_modes
            else []
        ),  # dense ramtx can be operated for querying either barcodes/features
        "version": _version_,
    }
    logger.info(
        f"Exporting of a RamData object at '{path_folder_ramdata_output}' was completed"
    )


""" a class for Zarr-based DataFrame object """


class ZarrDataFrame:
    """# 2023-05-06 01:10:12 
    storage-based persistant DataFrame backed by Zarr persistent arrays.
    each column can be separately loaded, updated, and unloaded.
    a filter can be set, which allows updating and reading ZarrDataFrame as if it only contains the rows indicated by the given filter.
    currently supported dtypes are bool, float, int, strings (will be interpreted as categorical data).
    the one of the functionality of this class is to provide a Zarr-based dataframe object that is compatible with Zarr.js (javascript implementation of Zarr), with a categorical data type (the format used in zarr is currently not supported in zarr.js) compatible with zarr.js.

    Of note, secondary indexing (row indexing) is always applied to unfiltered columns, not to a subset of column containing filtered rows.
    '__getitem__' function is thread and process-safe, while '__setitem__' is not thread nor prosess-safe.

    # 2022-07-04 10:40:14 implement handling of categorical series inputs/categorical series output. Therefore, convertion of ZarrDataFrame categorical data to pandas categorical data should occurs only when dataframe was given as input/output is in dataframe format.
    # 2022-07-04 10:40:20 also, implement a flag-based switch for returning series-based outputs
    # 2022-07-20 22:29:41 : masking functionality was added for the analysis of remote, read-only ZarrDataFrame
    # 2022-08-02 02:17:32 : will enable the use of multi-dimensional data as the 'column'. the primary axis of the data should be same as the length of ZarrDataFrame (the number of rows when no filter is active). By default, the chunking will be only available along the primary axis.
    # 2022-09-09 14:54:28 : will implement lazy-loading of combined and masked ZarrDataFrame, in order to improve performance when source ZarrDataFrame is hosted remotely.
    # 2022-11-14 23:49:50 : for usability, descriptions and associated metadata (for example, a list of contributors and data sources) will be included in the ZarrDataFrame metatadata

    dict_metadata_description : the dictionary containing metadata of the column with the following schema:
            'description' : a brief description of the column
            'authors' : a list of authors and contributors for the column

    === arguments ===
    path_folder_zdf : Union[ str, None ] = None # a folder to store persistant zarr dataframe. This argument is required unless 'zdf_template' has been given.
    'df' : input dataframe.
    int_num_cpus : int = 10, # the number of process for parallel processing of columns

    === settings that cannot be changed after initialization ===
    'flag_enforce_name_col_with_only_valid_characters' : if True, every column name should not contain any of the following invalid characters, incompatible with attribute names: '! @#$%^&*()-=+`~:;[]{}\|,<.>/?' + '"' + "'", if False, the only invalid character will be '/', which is incompatible with linux file system as file/folder name.
    'flag_store_string_as_categorical' : if True, for string datatypes, it will be converted to categorical data type.
    int_num_bytes_in_a_chunk : int = 320000 # a maximum number of bytes in a chunk for each data type to set a chunk size for the primary axis.

    === settings that can be changed anytime after initialization ===
    'ba_filter' : a bitarray object for applying filter for the ZarrDataFrame. 1 meaning the row is included, 0 meaning the row is excluded
                  If None is given (which is default), the filter is not applied, and the returned data will have the same number of items as the number of rows of the ZarrDataFrame
                  when a filter is active, setting new data and retrieving existing data will work as if the actual ZarrDataFrame is filtered and has the smaller number of rows.
                  A filter can be changed anytime after initialization of a ZarrDataFrame, but changing (including removing or newly applying filters) will remove all cached data, since the cache only contains data after apply filter to be memory-efficient.
                  A filter can be removed by setting 'filter' attribute to None

                  current implementation has following limits, which can be improved further:
                      - when a filter is active, slicing will load an entire column (after applying filter) (when filter is inactive, slicing will only load the data corresponding to the sliced region)
    'flag_retrieve_categorical_data_as_integers' : if True, accessing categorical data will return integer representations of the categorical values.
    'flag_load_data_after_adding_new_column' : if True, automatically load the newly added data to the object cache. if False, the newly added data will not be added to the object cache, and accessing the newly added column will cause reading the newly written data from the disk. It is recommended to set this to False if Zdf is used as a data sink
    'mode' : file mode. 'r' for read-only mode and 'a' for mode allowing modifications
    'path_folder_mask' : a local (local file system) path to the mask of the current ZarrDataFrame that allows modifications to be written without modifying the source. if a valid local path to a mask is given, all modifications will be written to the mask
    'flag_is_read_only' : read-only status of the storage
    'flag_use_mask_for_caching' : use mask for not only storing modifications, but also save retrieved data from (remote) sources for faster access. this behavior can be turned on/off at any time

    === settings for controlling buffer (batch) size ===
    'int_max_num_entries_per_batch' = 1000000 # the maximum number of entries to be processed in a batch (determines memory usage)

    === settings for combined ZarrDataFrame ===
    settings for combined ZarrDataFrames.
    When a list of ZarrDataFrame objects were given through the 'l_zdf' argument, 'combined' ZarrDataFrame mode will be activated.
    Briefly, combined ZarrDataFrame works by retrieving data from individual zdf objects, combined the data, and write a combined data as a column of 'combined' ZarrDataFrame.
    A combined column will be written to the current ZarrDataFrame every time data values were retrieved across the given list of zdf objects and combined (which can serve as a local cache, if one of the zdf object reside in remote location).

    There are two types of combined ZarrDataFrames, 'stacked' and 'interleaved'
        * 'stacked' : rows of each ZarrDataFrame stacked on top of each other without interleaving
            ----------
            rows of ZDF-0
            ----------
            rows of ZDF-1
            ----------
            rows of ZDF-2
            ...

        * 'interleaved' : rows of each ZarrDataFrame can be mapped to those of each other.ns[ 'l_buffer' ]

    'l_zdf' : a list of ZarrDataFrame objects that will be combined
    'index_zdf_data_source_when_interleaved' : the index of the zdf to retrieve data when combining mode is interleaved (rows shared between ZDFs)
    'l_dict_index_mapping_interleaved' : list of dictionaries mapping row indices of the combined ZarrDataFrame to row indices of each individual ZarrDataFrame. this argument should be set to non-None value only when the current combined ZarrDataFrame is interleaved. if None is given, the combined ZarrDataFrame will be considered 'stacked'
    zdf_template # a template to use for initialization of the ZarrDataFrame
    flag_mask : bool = False # if True, set the current ZarrDataFrame to be used as a mask. when 'flag_mask' is True, 'zdf_template' should be given, and 'path_folder_mask' should be given


    # arguments that works differently in combined zdf object
    'path_folder_zdf' : a path to the 'combined' ZarrDataFrame object.
    'int_num_rows' : when ZarrDataFrame is in combined mode and 'int_num_rows' argument is not given, 'int_num_rows' will be inferred from the given list of ZarrDataFrame 'l_zdf' and 'l_dict_index_mapping_interleaved'

    === arguments for mask operation ===
    'zdf_source' : reference to the ZarrDataFrame that will act as a data source for the current zdf

    === settings for lazy-loading ===
    flag_use_lazy_loading = True : if False, all values from a column from masked ZDF or combined ZDF will be retrieved and saved as a new column of the current ZDF even when a single entry was accessed.
        if True, based on the availability mask, only the accessed entries will be transferred to the current ZDF object, reducing significant overhead when the number of rows are extremely large (e.g. > 10 million entries)

    === Amazon S3/other file remote system ===
    dict_kwargs_credentials_s3 : dict = dict( ) # credentials for Amazon S3 object. By default, credentials will be retrieved from the default location.

    === Synchronization across multiple processes and (remote) devices analyzing the current ZarrDataFrame (multiple 'researchers') ===
    flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock : bool = False # if True, does not wait and raise 'RuntimeError' when a modification of a RamData cannot be made due to the resource that need modification is temporarily unavailable, locked by other processes
    float_second_to_wait_before_checking_availability_of_a_spin_lock : float = 0.5 # number of seconds to wait before repeatedly checking the availability of a spin lock if the lock has been acquired by other operations.
    zarrspinlockserver : Union[ True, None, ZarrSpinLockServer ] = None # a ZarrSpinLockServer object for synchronization of methods of the current object. if None is given, synchronization feature will not be used. if True is given, a new ZarrSpinLockServer object will be created and attached to the current ZarrDataFrame object
    flag_spawn : Union[ None, bool ] = None # by default, automatically determines whether 'spawn' method should be used during multiprocessing. When Zarr objects are located remotely, 'spawn' method will be used automatically.

    === Web application ===
    flag_store_64bit_integer_as_float : bool = True # currently, javascript implementation of Zarr does not support a 64bit integer datatype. By setting this flag to True, all data values using a 64bit integer datatype will be saved using the 64bit float datatype.


    notes:
        - column names ends with double underbar characters, including  '...__availability__' or '...__index__' are reserved for internal functions of ZarrDataFrame.
    """

    def __init__(
        self,
        path_folder_zdf: Union[str, None] = None,
        l_zdf: Union[list, tuple, None] = None,
        index_zdf_data_source_when_interleaved: int = 0,
        l_dict_index_mapping_interleaved: Union[List[dict], None] = None,
        l_dict_index_mapping_from_combined_to_component=None,
        l_dict_index_mapping_from_component_to_combined=None,
        int_max_num_entries_per_batch: int = 1000000,
        df: Union[pd.DataFrame, None] = None,
        int_num_rows: Union[int, None] = None,
        ba_filter: Union[bitarray, None] = None,
        flag_enforce_name_col_with_only_valid_characters: bool = False,
        flag_store_string_as_categorical: bool = True,
        flag_store_64bit_integer_as_float: bool = True,
        flag_retrieve_categorical_data_as_integers: bool = False,
        flag_load_data_after_adding_new_column: bool = True,
        mode: str = "a",
        path_folder_mask=None,
        zdf_source=None,
        flag_is_read_only: bool = False,
        flag_use_mask_for_caching: bool = True,
        verbose: bool = True,
        flag_use_lazy_loading: bool = True,
        dict_kwargs_credentials_s3: dict = dict(),
        flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock: bool = False,
        float_second_to_wait_before_checking_availability_of_a_spin_lock: float = 0.1,
        zarrspinlockserver: Union[None, bool, ZarrSpinLockServer] = None,
        int_num_bytes_in_a_chunk: int = 320000,
        flag_spawn: Union[None, bool] = None,
        int_num_cpus: int = 10,
        zdf_template=None,
        flag_mask: bool = False,
    ):
        """# 2023-04-26 20:53:38"""
        # set attributes from arguments
        if zdf_template is not None:
            # set attributes that can be changed anytime during the lifetime of the object
            self._dict_kwargs_credentials_s3 = zdf_template._dict_kwargs_credentials_s3
            self._flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock = (
                zdf_template._flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock
            )
            self._float_second_to_wait_before_checking_availability_of_a_spin_lock = (
                zdf_template._float_second_to_wait_before_checking_availability_of_a_spin_lock
            )
            self.flag_store_64bit_integer_as_float = (
                zdf_template.flag_store_64bit_integer_as_float
            )

            # settings that can be changed after initialization
            self._int_num_cpus = zdf_template._int_num_cpus
            self.flag_use_mask_for_caching = zdf_template.flag_use_mask_for_caching
            self.flag_retrieve_categorical_data_as_integers = (
                zdf_template.flag_retrieve_categorical_data_as_integers
            )
            self._path_folder_zdf = zdf_template._path_folder_zdf
            self._mode = zdf_template._mode
            self._flag_is_read_only = zdf_template._flag_is_read_only
            self._path_folder_mask = zdf_template._path_folder_mask
            self._flag_load_data_after_adding_new_column = (
                zdf_template._flag_load_data_after_adding_new_column
            )
            self._ba_filter = None  # initialize the '_ba_filter' attribute
            self.verbose = zdf_template.verbose
            self.int_max_num_entries_per_batch = (
                zdf_template.int_max_num_entries_per_batch
            )
            self._zdf_source = zdf_template._zdf_source
            self._flag_use_lazy_loading = zdf_template._flag_use_lazy_loading
            self._flag_spawn = (
                zdf_template._flag_spawn if flag_spawn is None else flag_spawn
            )  # prioritize argument over the settings of the template

            # retrieve filter object
            ba_filter = zdf_template._ba_filter  # initialize the '_ba_filter' attribute

            # %% COMBINED MODE %%
            self._l_zdf = zdf_template._l_zdf
            self.index_zdf_data_source_when_interleaved = (
                zdf_template.index_zdf_data_source_when_interleaved
            )
            self._l_dict_index_mapping_interleaved = (
                zdf_template._l_dict_index_mapping_interleaved
            )
            self._l_dict_index_mapping_from_combined_to_component = (
                zdf_template._l_dict_index_mapping_from_combined_to_component
            )
            self._l_dict_index_mapping_from_component_to_combined = (
                zdf_template._l_dict_index_mapping_from_component_to_combined
            )

            if (
                flag_mask and self._path_folder_mask is not None
            ):  # set the current ZarrDataFrame as a mask ZarrDataFrame
                # %% MASK %%
                self._path_folder_zdf = (
                    self._path_folder_mask
                )  # use path to the mask as the zdf path
                self._mode = ("a",)
                self._path_folder_mask = (None,)
                self._flag_is_read_only = (False,)
                self._zdf_source = (
                    zdf_template,
                )  # use the reference to the ZarrDataFrame used as a template  to current source zdf
        else:
            # set attributes that can be changed anytime during the lifetime of the object
            self._dict_kwargs_credentials_s3 = dict_kwargs_credentials_s3
            self._flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock = flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock
            self._float_second_to_wait_before_checking_availability_of_a_spin_lock = (
                float_second_to_wait_before_checking_availability_of_a_spin_lock
            )
            self.flag_store_64bit_integer_as_float = flag_store_64bit_integer_as_float

            # handle path
            if (
                "://" not in path_folder_zdf
            ):  # does not retrieve abspath if the given path is remote path
                path_folder_zdf = os.path.abspath(
                    path_folder_zdf
                )  # retrieve absolute path
            if (
                path_folder_zdf[-1] != "/"
            ):  # add '/' to the end of path to mark that this is a folder directory
                path_folder_zdf += "/"

            # settings that can be changed after initialization
            self._int_num_cpus = int_num_cpus
            self.flag_use_mask_for_caching = flag_use_mask_for_caching
            self.flag_retrieve_categorical_data_as_integers = (
                flag_retrieve_categorical_data_as_integers
            )
            self._path_folder_zdf = path_folder_zdf
            self._mode = mode
            self._flag_is_read_only = flag_is_read_only
            self._path_folder_mask = path_folder_mask
            self._flag_load_data_after_adding_new_column = (
                flag_load_data_after_adding_new_column
            )
            self._ba_filter = None  # initialize the '_ba_filter' attribute
            self.verbose = verbose
            self.int_max_num_entries_per_batch = int_max_num_entries_per_batch
            self._zdf_source = zdf_source
            self._flag_use_lazy_loading = flag_use_lazy_loading

            """ set multiprocessing methods """
            if flag_spawn is None:
                flag_spawn = self.is_remote
            self._flag_spawn = flag_spawn

            # %% COMBINED MODE %%
            self._l_zdf = l_zdf
            self.index_zdf_data_source_when_interleaved = (
                index_zdf_data_source_when_interleaved
            )
            self._l_dict_index_mapping_interleaved = l_dict_index_mapping_interleaved
            self._l_dict_index_mapping_from_combined_to_component = (
                l_dict_index_mapping_from_combined_to_component
            )
            self._l_dict_index_mapping_from_component_to_combined = (
                l_dict_index_mapping_from_component_to_combined
            )

        # initialize components
        self.fs = FileSystemServer(
            flag_spawn=self.flag_spawn,
            dict_kwargs_credentials_s3=self._dict_kwargs_credentials_s3,
        )  # initialize the file system server

        # load a zarr spin lock server depending on the settings
        # %% LOCKING %%
        if isinstance(zarrspinlockserver, ZarrSpinLockServer):
            self._zsls = zarrspinlockserver
        elif (
            zarrspinlockserver
        ):  # if 'zarrspinlockserver' is True, start a new zarr spin lock server (without spawning a new process)
            self._zsls = ZarrSpinLockServer(
                flag_spawn=self.flag_spawn,
                dict_kwargs_credentials_s3=self._dict_kwargs_credentials_s3,
                flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock=self._flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock,
                float_second_to_wait_before_checking_availability_of_a_spin_lock=self._float_second_to_wait_before_checking_availability_of_a_spin_lock,
                filesystem_server=self.fs,  # use the existing file system server.
            )
        else:  # if 'zarrspinlockserver' is False or None, does not use a synchronization feature
            self._zsls = None

        # load a zarr server for accessing Zarr objects
        self._zs = ZarrServer(None, flag_spawn=self.flag_spawn)

        # %% COMBINED = STACKED %%
        if self.is_combined and not self.is_interleaved:
            # retrieve the number of unfiltered rows for each zdf
            self._l_n_rows_unfiltered = list(
                zdf._n_rows_unfiltered for zdf in self._l_zdf
            )

        if (
            self.is_combined and int_num_rows is None
        ):  # infer 'int_num_rows' from the given arguments
            if self.is_interleaved:  # infer 'int_num_rows' for interleaved czdf
                int_num_rows = (
                    max(
                        max(dict_index)
                        for dict_index in self._l_dict_index_mapping_interleaved
                    )
                    + 1
                )  # 0 based -> 1 based length
            else:  # infer 'int_num_rows' for stacked czdf (combined zdf)
                int_num_rows = sum(
                    self._l_n_rows_unfiltered
                )  # assumes given zdf has valid number of rows

        # open or initialize zdf and retrieve associated metadata
        if not zarr_exists(
            self.path_folder
        ):  # if the object does not exist, initialize ZarrDataFrame
            # create the output folder
            self.fs.filesystem_operations("mkdir", self.path_folder, exist_ok=True)

            # set metadata
            self._dict_metadata = {
                "version": _version_,
                "columns": dict(),
                "flag_enforce_name_col_with_only_valid_characters": flag_enforce_name_col_with_only_valid_characters,
                "int_num_bytes_in_a_chunk": int_num_bytes_in_a_chunk,
                "flag_store_string_as_categorical": flag_store_string_as_categorical,
                "is_interleaved": self.is_interleaved,
                "is_combined": self.is_combined,
            }  # to reduce the number of I/O operations from lookup, a metadata dictionary will be used to retrieve/update all the metadata
            # if 'int_num_rows' has been given, add it to the metadata
            if int_num_rows is not None:
                self._dict_metadata["int_num_rows"] = int_num_rows
            self.set_metadata(self._dict_metadata)  # save metadata
        else:
            # retrieve metadata
            self._dict_metadata = self.get_metadata()

            """ %% TEMP %% """
            if "int_num_bytes_in_a_chunk" not in self._dict_metadata:
                # update metadata that were create before 2023-01-18 20:06:29
                del self._dict_metadata["int_num_rows_in_a_chunk"]
                self._dict_metadata[
                    "int_num_bytes_in_a_chunk"
                ] = int_num_bytes_in_a_chunk
                self.set_metadata(dict_metadata=self._dict_metadata)
            # handle the old versions of the zarrdataframe columns
            if "columns" in self._dict_metadata:
                if isinstance(self._dict_metadata["columns"], list):
                    self._dict_metadata["columns"] = dict(
                        (col, None) for col in self._dict_metadata["columns"]
                    )
                    self.set_metadata(self._dict_metadata)  # save metadata

        # apply filter once the zdf is properly initialized
        self.filter = ba_filter

        # if a mask is given, open the mask zdf
        self._mask = None  # initialize 'mask'
        if self._path_folder_mask is not None:  # if a mask is given
            # %% MASK %%
            self._mask = ZarrDataFrame(
                zdf_template=self,
                flag_mask=True,
                df=df,
            )  # the mask ZarrDataFrame shoud not have mask, should be modifiable, and not mode == 'r'.

        # handle input arguments
        self._str_invalid_char = (
            "<>:/\|?*" + '"' # reserved characters in Windows file system
            if self._dict_metadata["flag_enforce_name_col_with_only_valid_characters"]
            else "/" # reserved characters in Linux file system
        )

        # initialize loaded data
        self._loaded_data = (
            dict()
        )  # containing filtered data (if filter is active) or unfiltered data (if filter is not active)

        if isinstance(df, pd.DataFrame):  # if a valid pandas.dataframe has been given
            # update zdf with the given dataframe
            self.update(df)

        # initialize attribute storing columns as dictionaries
        self.dict = dict()

    @property
    def flag_spawn(self):
        """# 2023-04-16 22:02:49
        return the status of the current ZarrDataFrame object whether the spawn method is used for its operations
        """
        return self._flag_spawn

    def _ipython_key_completions_(self):
        """# 2023-01-21 14:50:07
        (ipython integration) method for supporting autocompletion of columns
        """
        return list(self.columns)

    def _get_folder_name_from_column_name( self, name_col : str ) :
        """ # 2023-05-05 22:51:50 
        get folder name (compatible with operating system) from column name, by replacing file-system-incompatible characters with escape characters.
        if the column name is incompatible with operating system (Linux, specifically), a 'FileNotFoundError' error will be raised.
        """
        return get_path_compatible_str( 
            str_input = name_col,
            str_invalid_char = self._str_invalid_char,
            int_max_num_bytes_in_a_folder_name = 255 - 5, # the maximum number of bytes for a folder name in Linux (255) # additional number of bytes (5) required for certain operations of the ZarrDataFrame object
        )
    @property
    def path_folder(self):
        """# 2023-04-12 17:19:28"""
        return self._path_folder_zdf

    @property
    def int_num_cpus(self):
        """# 2023-01-20 17:41:25
        number of cpu cores to use for ZarrDataFrame operations
        """
        return self._int_num_cpus

    @int_num_cpus.setter
    def int_num_cpus(self, val):
        """# 2023-01-20 17:41:25
        change the number of cpu cores to use for ZarrDataFrame operations
        """
        self._int_num_cpus = val
        if self._mask is not None:
            self._mask.int_num_cpus = val

    def __len__(self):
        """# 2022-09-22 23:45:53
        return the number of rows (after applying filter if a filter has been set)
        """
        return self.n_rows

    @property
    def locking_server(self):
        """# 2022-12-23 00:02:37
        return 'ZarrSpinLockServer' object
        """
        return self._zsls

    @locking_server.setter
    def locking_server(self, locking_server_new):
        """# 2023-01-19 13:05:20
        # replace the previous locking server with new locking server
        """
        self._zsls = (
            locking_server_new  # set 'ZarrSpinLockServer' of the current object
        )
        if self._mask is not None:  # set locking server of mask, too
            self._mask.locking_server = locking_server_new

    @property
    def is_remote(self):
        """# 2022-09-03 17:17:32
        return True if the RAMtx is located remotely
        """
        return is_remote_url(self.path_folder)

    @property
    def contains_remote(self):
        """# 2023-04-16 21:19:43
        return True if current RAMtx is in remote location or contains component RAMtx hosted remotely
        """
        # if current ZDF is in remote location, return True
        if self.is_remote:
            return True
        # if current ZDF is in combined mode, survey its component and identify ZDF located remotely
        if self.is_combined:
            for zdf in self._l_zdf:
                if zdf is not None and zdf.is_remote:
                    return True

    def get_fork_safe_version(self, flag_use_locking: bool = True):
        """# 2023-01-19 13:07:23
        return a fork-safe version of the current ZarrDataFrame

        flag_use_locking : bool = True # create a new 'ZarrSpinLockServer' object and attach the object to the new ZarrDataFrame object returned by the current function
        """
        # initialize and return a new ZarrDataFrame with new spawned components
        return ZarrDataFrame(
            zdf_template=self,
            flag_spawn=self.is_remote,
            zarrspinlockserver=True if flag_use_locking else None,
        )  # use spawning only for remote datasets

    def terminate_spawned_processes(self):
        """# 2022-12-08 18:59:11
        destroy zarr server objects if they exists in the current object
        """
        if not hasattr(
            self, "_flag_is_terminated"
        ):  # terminate the spawned processes only once
            # terminate the servers
            self.fs.terminate()
            if self._zsls is not None:
                self._zsls.terminate()
            self._zs.terminate()
            # terminate additional zarr servers
            if hasattr(self, "_zs_sink"):
                self._zs_sink.terminate()
            if hasattr(self, "_zs_source"):
                self._zs_source.terminate()
            self._flag_is_terminated = (
                True  # set a flag indicating spawned processes have been terminated.
            )

    @property
    def path_folder_zdf(self):
        """# 2022-12-11 22:38:21
        return 'path_folder_zdf' of the current object
        """
        return self._path_folder_zdf

    @property
    def is_mask(self):
        """# 2022-09-10 22:14:40
        return True if the current ZarrDataFrame will act as a mask of another ZarrDataFrame the act as a data source
        """
        return self._zdf_source is not None

    @property
    def is_combined(self):
        """# 2022-08-25 13:53:20
        return True if current zdf is in 'combined' mode
        """
        return self._l_zdf is not None

    @property
    def is_interleaved(self):
        """# 2022-08-25 14:03:34
        return True if current zdf is interleaved 'combined' zdf
        """
        return self._l_dict_index_mapping_interleaved is not None

    @property
    def is_remote(self):
        """# 2022-09-21 08:48:28
        return True if the ZDF is located remotely
        """
        return is_remote_url(self._path_folder_zdf)

    @property
    def contains_remote(self):
        """# 2022-09-21 08:48:33
        return True if current ZDF is in remote location or contains component ZDF hosted remotely
        """
        # if current zdf is in remote location, return True
        if self.is_remote:
            return True
        # if current zdf is in combined mode, survey its component and identify zdf located remotely
        if self.is_combined:
            for zdf in self._l_zdf:
                if zdf is not None and zdf.is_remote:
                    return True

    @property
    def flag_spawn(self):
        """# 2023-03-26 01:35:37
        return 'flag_spawn' attribute
        """
        return self._flag_spawn

    @property
    def int_num_bytes_in_a_chunk(self):
        """# 2022-08-02 13:01:53
        return the number of bytes in a chunk in the primary axis for each data type
        """
        return self._dict_metadata["int_num_bytes_in_a_chunk"]

    @int_num_bytes_in_a_chunk.setter
    def int_num_bytes_in_a_chunk(self, val):
        """# 2022-08-02 13:01:53
        setting the number of bytes in a chunk in the primary axis
        """
        self.update_metadata({"int_num_bytes_in_a_chunk": val})  # update metadata
        # update the settings of the mask, if available.
        if self._mask is not None:
            self._mask.int_num_bytes_in_a_chunk = val

    def get_int_num_rows_in_a_chunk(
        self,
        dtype,
        chunks_not_primary_axis: List = (),
        int_expected_length_of_string_for_string_dtype: int = 50,
    ):
        """# 2023-01-18 19:20:53
        calculate 'int_num_rows_in_a_chunk' for the given 'dtype' and 'chunks_not_primary_axis' pair using the internal 'dict_data_type_to_int_num_values_in_a_chunk' settings.

        dtype # 'category', bool, and other dtypes (default) will be used
        int_expected_length_of_string_for_string_dtype : int = 50 # the default number of character for a string of variable length for a string dtype.
        """
        # retrieve 'int_num_bits_in_a_value'
        if dtype == str:  # for a string dtype
            int_num_bits_in_a_value = (
                int_expected_length_of_string_for_string_dtype * 8
            )  # assumes 1 character uses 1 byte, which is 8 bits
        elif dtype == bool:  # for a boolean dtype
            int_num_bits_in_a_value = 1  # boolean dtype use 1 bit when using zarr
        else:  # handle other numpy dtypes
            try:
                int_num_bits_in_a_value = (
                    np.dtype(dtype).itemsize * 8
                )  # the unit of the itemsize is bytes
            except:
                logger.info(f"invalid {dtype = } was given, exiting")
                return

        # retrieve 'int_num_values_in_a_chunk'
        int_num_values_in_a_chunk = int(
            np.ceil(self.int_num_bytes_in_a_chunk * 8 / int_num_bits_in_a_value)
        )  # using ceiling method to determine the number of values in a chunk in the primary axis.

        # retrieve 'int_num_values_in_a_row'
        if (
            len(chunks_not_primary_axis) == 0
        ):  # by default, there will be one value for each row
            chunks_not_primary_axis = [1]
        int_num_values_in_a_row = np.prod(list(chunks_not_primary_axis))

        int_num_rows_in_a_chunk = int(
            np.ceil(int_num_values_in_a_chunk / int_num_values_in_a_row)
        )  # using ceiling method to determine the number of rows in a chunk in the primary axis.
        return int_num_rows_in_a_chunk

    @property
    def _n_rows_unfiltered(self):
        """# 2022-06-22 23:12:09
        retrieve the number of rows in unfiltered ZarrDataFrame. return None if unavailable.
        """
        if (
            "int_num_rows" not in self._dict_metadata
        ):  # if 'int_num_rows' has not been set, return None
            return None
        else:  # if 'int_num_rows' has been set
            return self._dict_metadata["int_num_rows"]

    @property
    def n_rows(self):
        """# 2022-06-22 16:36:54
        retrieve the number of rows after applying filter. if the filter is not active, return the number of rows of the unfiltered ZarrDataFrame
        """
        if (
            self.filter is None
        ):  # if the filter is not active, return the number of rows of the unfiltered ZarrDataFrame
            return self._n_rows_unfiltered
        else:  # if a filter is active
            return (
                self._n_rows_after_applying_filter
            )  # return the number of active rows in the filter

    @property
    def filter(self):
        """# 2022-06-22 16:36:22
        return filter bitarray"""
        return self._ba_filter

    @filter.setter
    def filter(self, ba_filter):
        """# 2022-08-25 17:17:58
        change filter, and empty the cache
        """
        if ba_filter is None:  # if filter is removed,
            # if the filter was present before the filter was removed, empty the cache and the temp folder
            if self.filter is not None:
                self._loaded_data = dict()  # empty the cache
                self.dict = dict()  # empty the cache for columns stored as dictionaries
            self._ba_filter = None
            self._n_rows_after_applying_filter = None
        else:
            # check whether the given filter is bitarray
            if isinstance(ba_filter, np.ndarray):  # convert numpy array to bitarray
                ba_filter = BA.to_bitarray(ba_filter)
            assert isinstance(
                ba_filter, bitarray
            )  # make sure that the input value is a bitarray object

            # check the length of filter bitarray
            if (
                "int_num_rows" not in self._dict_metadata
            ):  # if 'int_num_rows' has not been set, set 'int_num_rows' using the length of the filter bitarray
                self.update_metadata(
                    dict_metadata_to_be_updated={"int_num_rows": len(ba_filter)}
                )  # save metadata
            else:
                # check the length of filter bitarray
                assert len(ba_filter) == self._dict_metadata["int_num_rows"]

            self._loaded_data = dict()  # empty the cache
            self.dict = dict()  # empty the cache for columns stored as dictionaries
            self._n_rows_after_applying_filter = (
                ba_filter.count()
            )  # retrieve the number of rows after applying the filter

            self._ba_filter = ba_filter  # set bitarray filter
        # set filter of mask
        if (
            hasattr(self, "_mask") and self._mask is not None
        ):  # propagate filter change to the mask ZDF
            self._mask.filter = ba_filter

        if self.is_combined:
            # %% COMBINED %%
            if ba_filter is None:  # if filter is removed
                # remove filter from all zdf objects
                for zdf in self._l_zdf:
                    zdf.filter = None
            else:  # if filter is being set
                if self.is_interleaved:
                    # %% COMBINED - INTERLEAVED %%
                    for zdf, dict_index_mapping_interleaved in zip(
                        self._l_zdf, self._l_dict_index_mapping_interleaved
                    ):
                        # initialize filter for the current zdf object
                        ba_zdf = bitarray(zdf._n_rows_unfiltered)
                        ba_zdf.setall(0)
                        # compose filter
                        for int_entry_combined in BA.find(
                            ba_filter
                        ):  # iterate active entries in the combined axis
                            if (
                                int_entry_combined in dict_index_mapping_interleaved
                            ):  # if the active entry also exists in the current axis, update the filter
                                ba_zdf[
                                    dict_index_mapping_interleaved[int_entry_combined]
                                ] = 1

                        zdf.filter = ba_zdf  # set filter
                else:
                    # %% COMBINED - STACKED %%
                    # for stacked czdf, split the given filter into smaller filters for each zdf
                    int_pos = 0
                    for zdf in self._l_zdf:
                        zdf.filter = ba_filter[
                            int_pos : int_pos + zdf._n_rows_unfiltered
                        ]  # apply a subset of filter
                        int_pos += zdf._n_rows_unfiltered  # update 'int_pos'

    """ <Methods handling columns> """

    @property
    def metadata_columns(self):
        """# 2023-04-28 04:45:46
        return the value of 'columns' key from the metadata of the current axis and its component axes.
        """
        # initialize metadata of the columns
        metadata_columns = dict()
        # retrieve metadata of the columns
        metadata_columns = (
            self.metadata["columns"] | metadata_columns
        )  # add metadata of the columns of the current ZDF
        # add metadata of the columns of mask
        if self._mask is not None:  # if mask is available :
            metadata_columns = (
                self._mask.metadata["columns"] | metadata_columns
            )  # add metadata of the columns of the mask ZDF
        # add metadata of the columns from zdf components
        if self.is_combined:
            if self.is_interleaved:
                # %% COMBINED INTERLEAVED %%
                zdf = self._l_zdf[
                    self.index_zdf_data_source_when_interleaved
                ]  # retrieve data source zdf
                metadata_columns = (
                    zdf.metadata_columns | metadata_columns
                )  # add metadata of the columns of the data source zdf
            else:
                # %% COMBINED STACKED %%
                for zdf in self._l_zdf:  # for each zdf component
                    metadata_columns = (
                        zdf.metadata_columns | metadata_columns
                    )  # add metadata of the columns of the zdf component
        return metadata_columns

    @property
    def metadata_columns_excluding_components(self):
        """# 2023-04-28 04:45:50
        return the value of 'columns' key from the metadata of the current axis.
        """
        # initialize metadata of the columns
        metadata_columns = dict()
        # retrieve metadata of the columns
        metadata_columns = (
            self.metadata["columns"] | metadata_columns
        )  # add metadata of the columns of the current ZDF
        # add metadata of the columns of mask
        if self._mask is not None:  # if mask is available :
            metadata_columns = (
                self._mask.metadata["columns"] | metadata_columns
            )  # add metadata of the columns of the mask ZDF
        return metadata_columns

    @property
    def columns(self):
        """# 2023-02-14 23:39:01
        return available column names (including mask and components) as a set
        """
        return set(self.metadata_columns)

    @property
    def columns_excluding_components(self):
        """# 2023-02-14 23:39:05
        return available column names (including mask but excluding components) as a set
        """
        return set(self.metadata_columns_excluding_components)

    def __contains__(self, name_col: str):
        """# 2023-02-23 21:35:20
        check whether a column name exists in the given ZarrDataFrame
        """
        return name_col in self.metadata_columns

    def __iter__(self):
        """# 2022-11-15 00:55:57
        iterate name of columns in the current ZarrDataFrame
        """
        if self._mask is not None:  # if mask is available :
            return iter(
                set(self.columns).union(set(self._mask.columns))
            )  # iterate over the column names of the current ZDF and the mask ZDF
        else:
            return iter(self.columns)

    def _get_column_path(self, name_col: str, flag_exclude_components: bool = False):
        """# 2022-08-26 10:34:35
        if 'name_col' column exists in the current ZDF object, return the path of the column. the columns in mask, or component ZarrDataFrame will be found and retrieved.

        === arguments ===
        'name_col' : the name of the column to search
        flag_exclude_components : bool = False # the exclude columns that only exist in the ZarrDataFrame components

        the column will be searched in the following order: main zdf object --> mask zdf object --> component zdf objects, in the order specified in the list.
        """
        path_col = None  # set default value
        if (
            name_col is not None and name_col in self
        ):  # use 'name_col' as a template if valid name_col has been given
            name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve the name of the folder
            if name_col in self._dict_metadata["columns"]:  # search the current zdf
                path_col = f"{self._path_folder_zdf}{name_folder}/"
            elif (
                self._mask is not None
                and name_col in self._mask._dict_metadata["columns"]
            ):  # search mask (if available)
                path_col = f"{self._mask._path_folder_zdf}{self._mask._get_folder_name_from_column_name( name_col )}/"
            elif (
                self.is_combined and not flag_exclude_components
            ):  # search component zdf(s) (if combined mode is active) # ignore columns in the component ZarrDataFrame objects if 'flag_exclude_components' is True.
                if self.is_interleaved:
                    # %% COMBINED INTERLEAVED %%
                    zdf = self._l_zdf[
                        self.index_zdf_data_source_when_interleaved
                    ]  # retrieve data source zdf
                    path_col = f"{zdf._path_folder_zdf}{name_folder}/"
                else:
                    # %% COMBINED STACKED %%
                    for zdf in self._l_zdf:  # for each zdf component
                        if name_col in zdf:  # when the column was identified
                            path_col = f"{zdf._path_folder_zdf}{name_folder}/"
                            break
        return path_col  # return the path of the matched column

    """ <Methods handling columns> """
    """ <Methods handling Metadata> """

    @property
    def use_locking(self):
        """# 2022-12-12 02:45:43
        return True if a spin lock algorithm is being used for synchronization of operations on the current object
        """
        return self._zsls is not None

    @property
    def metadata(self):
        """# 2022-07-21 02:38:31"""
        return self.get_metadata()

    def get_metadata(self):
        """# 2022-12-13 02:00:26
        read metadata with file-locking
        """
        if (
            self.use_locking
        ):  # when locking has been enabled, read metadata from the storage, and update the metadata currently loaded in the memory
            self._zsls.wait_lock(
                f"{self._path_folder_zdf}.zattrs.lock/"
            )  # wait until a lock is released
            self._dict_metadata = self._zsls.zms.get_metadata(
                self._path_folder_zdf, "dict_metadata"
            )  # retrieve metadata from the storage, and update the metadata stored in the object
        elif not hasattr(
            self, "_dict_metadata"
        ):  # when locking is not used but the metadata has not been loaded, read the metadata without using the locking algorithm
            self._zs.open(self.path_folder, mode="r")
            self._dict_metadata = self._zs.get_attr(
                "dict_metadata"
            )  # retrieve 'dict_metadata' from the storage
        return self._dict_metadata  # return the metadata

    def set_metadata(self, dict_metadata: dict):
        """# 2022-12-11 22:08:05
        write metadata with file-locking
        """
        if (
            self._flag_is_read_only
        ):  # save metadata only when it is not in the read-only mode
            return
        self._dict_metadata = dict_metadata  # update metadata stored in the memory
        if self.use_locking:  # when locking has been enabled
            self._zsls.acquire_lock(
                f"{self._path_folder_zdf}.zattrs.lock/"
            )  # acquire a lock
            self._zsls.zms.set_metadata(
                self._path_folder_zdf, "dict_metadata", self._dict_metadata
            )  # write metadata to the storage
            self._zsls.release_lock(
                f"{self._path_folder_zdf}.zattrs.lock/"
            )  # release the lock
        else:  # if locking is not used, return previously loaded metadata
            self._zs.open(self.path_folder, mode="a")
            self._zs.set_attrs(dict_metadata=self._dict_metadata)  # set attributes

    def update_metadata(
        self,
        dict_metadata_to_be_updated: dict = dict(),
        l_name_col_to_be_deleted: list = [],
        dict_rename_name_col: dict = dict(),
    ):
        """# 2023-04-19 17:41:15
        write metadata with file-locking

        dict_metadata_to_be_updated : dict # a dictionarty for updating 'dict_metadata' of the current object
        l_name_col_to_be_deleted : list = [ ] # a list of name of columns to be deleted from the metadata.
        dict_rename_name_col : dict = dict( ) # a dictionary mapping previous name_col to new name_col for renaming columns
        """
        if (
            self._flag_is_read_only
        ):  # update the metadata only when it is not in the read-only mode
            return

        def __update_dict_metadata(
            dict_metadata: dict,
            dict_metadata_to_be_updated: dict,
            l_name_col_to_be_deleted: list,
            dict_rename_name_col: dict,
        ):
            """# 2022-12-11 23:38:13
            update dict_metadata with dict_metadata_to_be_updated and return the updated dict_metadata
            """
            if "columns" in dict_metadata_to_be_updated:
                dict_metadata_columns = dict_metadata["columns"]
                dict_metadata_columns.update(dict_metadata_to_be_updated["columns"])
                dict_metadata_to_be_updated["columns"] = dict_metadata_columns

            # update 'dict_metadata'
            dict_metadata.update(dict_metadata_to_be_updated)

            # delete columns from the 'dict_metadata'
            for name_col in l_name_col_to_be_deleted:
                if name_col in dict_metadata["columns"]:
                    dict_metadata["columns"].pop(name_col)

            # rename columns of the 'dict_metadata'
            for name_col_prev in dict_rename_name_col:
                name_col_new = dict_rename_name_col[name_col_prev]
                if (
                    name_col_prev in dict_metadata["columns"]
                    and name_col_new not in dict_metadata["columns"]
                ):  # for a valid pair of previous and new column names
                    dict_metadata["columns"][name_col_new] = dict_metadata[
                        "columns"
                    ].pop(
                        name_col_prev
                    )  # perform a renaming operation

            return dict_metadata

        if (
            self._zsls is None
        ):  # if locking is not used, return previously loaded metadata
            self._dict_metadata = __update_dict_metadata(
                self._dict_metadata,
                dict_metadata_to_be_updated,
                l_name_col_to_be_deleted,
                dict_rename_name_col,
            )  # update 'self._dict_metadata' with 'dict_metadata_to_be_updated'
            self._zs.open(self.path_folder, mode="a")
            self._zs.set_attrs(dict_metadata=self._dict_metadata)  # set attributes
        else:  # when locking has been enabled
            self._zsls.acquire_lock(
                f"{self._path_folder_zdf}.zattrs.lock/"
            )  # acquire a lock

            self._dict_metadata = self._zsls.zms.get_metadata(
                self._path_folder_zdf, "dict_metadata"
            )  # read metadata from the storage and update the metadata
            self._dict_metadata = __update_dict_metadata(
                self._dict_metadata,
                dict_metadata_to_be_updated,
                l_name_col_to_be_deleted,
                dict_rename_name_col,
            )  # update 'self._dict_metadata' with 'dict_metadata_to_be_updated'
            self._zsls.zms.set_metadata(
                self._path_folder_zdf, "dict_metadata", self._dict_metadata
            )  # write metadata to the storage

            self._zsls.release_lock(
                f"{self._path_folder_zdf}.zattrs.lock/"
            )  # release the lock

    def get_column_metadata(self, name_col: str):
        """# 2023-05-06 00:35:09 
        get metadata of a given column
        """
        if (
            name_col in self.columns_excluding_components
        ):  # if the current column is present in the current object
            name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve the name of the folder
            # if mask is available return the metadata from the mask
            if (
                self._mask is not None and name_col in self._mask
            ):  # if the column is available in the mask
                return self._mask.get_column_metadata(name_col=name_col)

            # %% FILE LOCKING %%
            if (
                self._zsls is not None
            ):  # if locking is used, wait until lock is released
                self._zsls.wait_lock(
                    f"{self._path_folder_zdf}{name_folder}.lock/"
                )  # wait until a lock is released

            # read metadata
            self._zs.open(
                f"{self._path_folder_zdf}{name_folder}/", mode="r"
            )  # read data from the Zarr object
            dict_col_metadata = self._zs.get_attr(
                "dict_col_metadata"
            )  # retrieve metadata of the current column
            return dict_col_metadata

    def set_column_metadata(self, name_col: str, dict_col_metadata: dict):
        """# 2023-05-06 00:35:14 
        a method for setting metadata of a given column (and the metadata of the current object)
        """
        if (
            name_col in self.columns_excluding_components
        ):  # if the column is located in the current object
            name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve the name of the folder
            # if mask is available return the metadata from the mask
            if (
                self._mask is not None and name_col in self._mask
            ):  # if the column is available in the mask
                return self._mask.set_column_metadata(
                    name_col=name_col, dict_col_metadata=dict_col_metadata
                )

            # %% FILE LOCKING %%
            if self.use_locking:  # if locking is used, acquire the lock
                flag_lock_acquired = self._zsls.acquire_lock(
                    f"{self._path_folder_zdf}{name_folder}.lock/"
                )  # wait until a lock is released

            try:
                # read column metadata
                self._zs.open(
                    f"{self._path_folder_zdf}{name_folder}/", mode="a"
                )  # open the Zarr object
                self._zs.set_attrs(
                    dict_col_metadata=dict_col_metadata
                )  # set metadata of the current column

                if "dict_metadata_description" in dict_col_metadata:
                    # update metadata (sycn. with metadata of the current object)
                    self.update_metadata(
                        {
                            "columns": {
                                name_col: dict_col_metadata["dict_metadata_description"]
                            }
                        }
                    )
            finally:
                # %% FILE LOCKING %%
                if self.use_locking:  # if locking is used, release the lock
                    if flag_lock_acquired:
                        self._zsls.release_lock(
                            f"{self._path_folder_zdf}{name_folder}.lock/"
                        )  # wait until a lock is released

    def update_column_metadata(
        self,
        name_col: str,
        dict_col_metadata_to_be_updated: dict,
        flag_relpace_dict_metadata_description: bool = False,
    ):
        """# 2023-04-20 16:13:56
        a method for setting metadata of a given column (and the metadata of the current object)

        dict_col_metadata_to_be_updated : dict # a dictionarty for updating 'dict_col_metadata'
        flag_relpace_dict_metadata_description : bool = False # if True, replace previous 'dict_col_metadata_description' with the current 'dict_col_metadata_description'. if False, update the previous 'dict_col_metadata_description' with the current 'dict_col_metadata_description'
        """
        if (
            name_col in self.columns_excluding_components
        ):  # if the column is present in the current object
            name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve the name of the folder
            # if mask is available return the metadata from the mask
            if (
                self._mask is not None and name_col in self._mask
            ):  # if the column is available in the mask
                return self._mask.update_column_metadata(
                    name_col=name_col,
                    dict_col_metadata_to_be_updated=dict_col_metadata_to_be_updated,
                )

            # %% FILE LOCKING %%
            if self.use_locking:  # if locking is used, acquire the lock
                flag_lock_acquired = self._zsls.acquire_lock(
                    f"{self._path_folder_zdf}{name_folder}.lock/"
                )  # wait until a lock is released

            try:
                # read metadata
                self._zs.open(
                    f"{self._path_folder_zdf}{name_folder}/", mode="a"
                )  # read data from the Zarr object
                dict_col_metadata = self._zs.get_attr(
                    "dict_col_metadata"
                )  # get attributes

                # update 'dict_col_metadata_description'
                if (
                    "dict_metadata_description" in dict_col_metadata_to_be_updated
                ):  # if 'dict_col_metadata_to_be_updated' contains 'dict_metadata_description' for the update
                    dict_metadata_description = (
                        dict_col_metadata["dict_metadata_description"]
                        if "dict_metadata_description" in dict_col_metadata
                        else dict()
                    )  # retrieve 'dict_col_metadata_description' from 'dict_col_metadata'
                    if isinstance(
                        dict_col_metadata_to_be_updated["dict_metadata_description"],
                        dict,
                    ):  # if dict_col_metadata_to_be_updated[ 'dict_metadata_description' ] contains valid value
                        if not isinstance(
                            dict_metadata_description, dict
                        ):  # initialize 'dict_metadata_description'
                            dict_metadata_description = dict()
                        dict_metadata_description.update(
                            dict_col_metadata_to_be_updated["dict_metadata_description"]
                        )  # update 'dict_col_metadata_description' using the 'dict_col_metadata_description' from the 'dict_col_metadata_to_be_updated'
                    else:  # reset 'dict_metadata_description'
                        dict_metadata_description = None
                    dict_col_metadata_to_be_updated[
                        "dict_metadata_description"
                    ] = dict_metadata_description  # set the updated 'dict_col_metadata_description'

                    # update metadata (sycn. with metadata of the current object)
                    self.update_metadata(
                        {"columns": {name_col: dict_metadata_description}}
                    )

                dict_col_metadata.update(
                    dict_col_metadata_to_be_updated
                )  # update 'dict_col_metadata'
                self._zs.set_attrs(
                    dict_col_metadata=dict_col_metadata
                )  # save the column metadata
            finally:
                # %% FILE LOCKING %%
                if self.use_locking:  # if locking is used, release the lock
                    if flag_lock_acquired:
                        self._zsls.release_lock(
                            f"{self._path_folder_zdf}{name_folder}.lock/"
                        )  # wait until a lock is released

    def get_column_metadata_description(self, name_col: str):
        """# 2022-12-05 12:00:53
        retrieve description metadata of a given column. (might not be up-to-date.)
        """
        if (
            name_col in self.columns_excluding_components
        ):  # if the column is present in the current object
            if self._zsls is not None:
                # %% FILE LOCKING %%
                return self.get_column_metadata(name_col)[
                    "dict_metadata_description"
                ]  # read column metadata from the storage
            else:
                # when file locking is not used, return column_metadata_description from the metadata of the current object
                return self._dict_metadata["columns"][
                    name_col
                ]  # return description metadata

    def update_column_metadata_description(
        self,
        name_col: str,
        dict_col_metadata_description_to_be_updated: Union[None, dict] = None,
    ):
        """# 2022-12-05 11:59:50
        update description metadata of a given column.

        dict_col_metadata_description_to_be_updated : Union[ None, dict ] = None # description about the column to be updated. Set to None or an empty dictionary will not update the description metadata

        (internally, ZDF metadata and individual column metadata will be modified)
        """
        if (
            name_col in self.columns_excluding_components
        ):  # if the column is present in the current object
            self.update_column_metadata(
                name_col=name_col,
                dict_col_metadata_to_be_updated={
                    "dict_metadata_description": dict_col_metadata_description_to_be_updated
                },
                flag_relpace_dict_metadata_description=False,
            )  # update previous 'dict_col_metadata_description' with the current 'dict_col_metadata_description'

    def set_column_metadata_description(
        self, name_col: str, dict_col_metadata_description: Union[None, dict] = None
    ):
        """# 2022-12-05 12:08:35
        set description metadata of a given column

        dict_col_metadata_description_to_be_updated : Union[ None, dict ] = None # description about the column to be updated. Set to None or an empty dictionary to delete a description about the column

        (internally, ZDF metadata and individual column metadata will be modified)
        """
        if (
            name_col in self.columns_excluding_components
        ):  # if the column is present in the current object
            self.update_column_metadata(
                name_col=name_col,
                dict_col_metadata_to_be_updated={
                    "dict_metadata_description": dict_col_metadata_description
                },
                flag_relpace_dict_metadata_description=True,
            )  # replace previous 'dict_col_metadata_description' with the current 'dict_col_metadata_description'

    def _add_column(
        self, name_col: str, dict_metadata_description: Union[dict, None] = None
    ):
        """# 2022-11-15 00:14:14
        a semi-private method for adding column label to the metadata of the current ZarrDataFrame (not added to the metadata of the mask)

        dict_metadata_description : Union[ str, None ] = None # 'dict_metadata_description' of the column. if None, no description metadata will be recorded
        """
        if (
            name_col not in self.columns_excluding_components
        ):  # if the column is not present in the current object
            self.update_metadata(
                dict_metadata_to_be_updated={
                    "columns": {name_col: dict_metadata_description}
                }
            )

    def _save_metadata_(self):
        """# 2022-11-15 00:14:34
        save metadata of the current ZarrDataFrame
        """
        if (
            not self._flag_is_read_only
        ):  # save metadata only when it is not in the read-only mode
            self.set_metadata(dict_metadata=self._dict_metadata)  # update metadata

    def get_categories(self, name_col: str):
        """# 2022-12-12 01:09:37
        for columns with categorical data, return categories. if the column contains non-categorical data, return an empty list
        """
        if (
            name_col in self.columns_excluding_components
        ):  # if the column is present in the current object
            # if the column is available in the mask, return the result of the mask
            if self._mask is not None and name_col in self._mask:
                return self._mask.get_categories(name_col=name_col)

            dict_col_metadata = self.get_column_metadata(
                name_col
            )  # retrieve metadata of the current column
            if dict_col_metadata[
                "flag_categorical"
            ]:  # if the current column contains categorical data
                return dict_col_metadata["l_value_unique"]
            else:
                return []

    """ </Methods handling Metadata> """

    def lazy_load(
        self,
        queries,
        flag_mode_write: bool = False,
        name_col_sink: Union[str, None] = None,
        path_column_sink: Union[str, None] = None,
        path_column_source: Union[str, None] = None,
        l_path_column_source: Union[list, None] = None,
        name_col_availability: Union[None, str] = None,
        flag_retrieve_from_all_interleaved_components: bool = False,
    ) -> None:
        """# 2023-05-06 03:44:27 
        perform lazy-loading of a given column using the column containing availability values.
        it will automatically detect the source objects based on the current setting.

        # ** warning ** : assumes component ZDF objects contain fully-loaded columns

        === general ===
        'queries' : queries for the 'get_integer_indices' method for retrieving the list of integer representations of the entries to load/update
        'name_col_sink' : the name of the column that will be used as a data sink.
        'flag_mode_write' : if True, only update availability column and the metadata.

        === arguments for managing external locations ===
        'path_column_sink' : the path to a writable zarr object that can be used as a data sink. the column will be annotated with zarrdataframe column metadata for lazy-loading operation.
        'path_column_source' : the path of source column from which data will be retrieved when 'mask' mode is used.
        'l_path_column_source' : A list of source columns from which data will be retrieved when 'combined' mode is used. these columns should be have the same length as the given list of component ZarrDataFrame objects
        'name_col_availability' : by default (if None will be given), default availability column name will be used. alternatively, a column name in the current ZarrDataFrame can be given (if it does not exists, it will be initialized)

        === when fetching from combined components ===
        'flag_retrieve_from_all_interleaved_components' : bool = False # if True, retrieve data from all components in the combined-interleaved ZDF
        """
        # load additional zarr servers for accessing Zarr objects
        if not hasattr(self, "_zs_sink"):
            self._zs_sink = ZarrServer(None, flag_spawn=self.flag_spawn)
        if not hasattr(self, "_zs_source"):
            self._zs_source = ZarrServer(None, flag_spawn=self.flag_spawn)
        # retrieve zarr server objects
        za_source, za_sink = self._zs_source, self._zs_sink

        # if mask is present, return the result of the mask
        if self._mask is not None:
            return self._mask.lazy_load(
                queries=queries,
                flag_mode_write=flag_mode_write,
                name_col_sink=name_col_sink,
                path_column_sink=path_column_sink,
                path_column_source=path_column_source,
                l_path_column_source=l_path_column_source,
                name_col_availability=name_col_availability,
                flag_retrieve_from_all_interleaved_components=flag_retrieve_from_all_interleaved_components,
            )

        if name_col_sink is None and path_column_sink is None:
            if self.verbose:
                logger.info(
                    f"[ZDF][lazy_load] sink column cannot be identified, exiting"
                )
            return
        # check whether the sink column is being lazy-loaded
        path_column_sink = (
            f"{self._path_folder_zdf}{self._get_folder_name_from_column_name( name_col_sink )}/" # retrieve the name of the folder
            if path_column_sink is None
            else path_column_sink
        )
        if zarr_exists(path_column_sink):
            za_sink.open(path_column_sink, mode="r")
            dict_attrs = za_sink.get_attrs(
                "flag_is_being_lazy_loaded"
            )  # retrieve attributes
            if (
                "flag_is_being_lazy_loaded" not in dict_attrs
            ):  # if the column has not been marked with a flag indicating lazy-loading has been started, exit
                return
            elif not dict_attrs[
                "flag_is_being_lazy_loaded"
            ]:  # if lazy-loading has been completed, exit
                return

        # handle invalid inputs
        if name_col_sink is not None:
            if (
                name_col_sink[-len("__availability__") :] == "__availability__"
            ):  # availability column should not be lazy-loaded
                return
            if self.is_combined and name_col_sink not in self.columns:
                return
            if self.is_mask and name_col_sink not in self._zdf_source.columns:
                return

        # handle invalid modes
        if not (
            self.is_combined or self.is_mask
        ):  # if source data is not available for the current ZarrDataFrame object, exit
            return

        # retrieve a flag indicating all entries will be available in the sink column
        flag_will_be_fully_loaded = isinstance(queries, slice) and queries == slice(
            None, None, None
        )

        # retrieve list of integer representations of the entries
        l_int_entry = list(self.get_integer_indices(queries))

        # retrieve operation modes
        flag_mode_internal = (
            name_col_sink is not None
        )  # 'internal locations' or 'external locations'

        if flag_mode_internal:  # retrieve internal locations
            if name_col_sink is None:  # check validity of input setting
                if self.verbose:
                    logger.info(
                        f"[ZDF][lazy_load] internal mode is active, but 'name_col_sink' has not been given"
                    )
                return
            name_folder_sink = self._get_folder_name_from_column_name( name_col_sink ) # retrieve the name of the folder
            path_column_sink = f"{self._path_folder_zdf}{name_folder_sink}/"
            name_col_availability = f"{name_col_sink}__availability__"
            if (
                self.is_combined and l_path_column_source is None
            ):  # if combined mode is active, pathes of the input component zarr objects will be retrieved
                l_path_column_source = list(
                    f"{self._path_folder_zdf}{name_folder_sink}/"
                    if name_col_sink in zdf
                    else None
                    for zdf in self._l_zdf
                )
            if (
                self.is_mask
            ):  # if mask mode is active, path of the source column will be retrieved
                path_column_source = (
                    f"{self._zdf_source._path_folder_zdf}{name_folder_sink}"
                )
        if name_col_availability is None:
            if self.verbose:
                logger.info(
                    f"[ZDF][lazy_load] 'name_col_availability' has not been given"
                )
            return

        # initialize sink column
        if flag_mode_write and not zarr_exists(
            path_column_sink
        ):  # if sink column does not exist
            # initialize sink column by retrieving the value of the first entry
            self.lazy_load(
                queries=[0],
                flag_mode_write=False,
                name_col_sink=name_col_sink,
                path_column_sink=path_column_sink,
                path_column_source=path_column_source,
                l_path_column_source=l_path_column_source,
                name_col_availability=name_col_availability,
            )  # 'read' mode

        # initialize availability column
        if (
            name_col_availability not in self
        ):  # if 'name_col_availability' column does not exist, initialize the column
            self.initialize_column(name_col_availability, dtype=bool, fill_value=False)
        dict_col_metadata_availbility = self.get_column_metadata(
            name_col_availability
        )  # retrieve metadata
        if (
            "flag_is_availability_column" not in dict_col_metadata_availbility
        ):  # initialize metadata for availability column
            # initialize metadata for availability column
            dict_col_metadata_availbility["flag_is_availability_column"] = True
            dict_col_metadata_availbility["int_num_entries_available"] = 0

        if flag_mode_write:  # for write operation
            # update availability column for the sink column (write operation)
            dict_col_metadata_availbility["int_num_entries_available"] += np.sum(
                ~self[name_col_availability, l_int_entry]
            )  # update the number of entries available
            # update availability
            if (
                not flag_will_be_fully_loaded
            ):  # if the column will be fully loaded, do not update the availability column
                self[
                    name_col_availability, l_int_entry
                ] = True  # update availability column
        else:
            # retrieve values from source and update sink column (read operation)
            l_int_entry_that_needs_fetching = np.array(l_int_entry, dtype=int)[
                ~self[name_col_availability, l_int_entry]
            ]  # retrieve int_entry that need updates
            if len(l_int_entry_that_needs_fetching) > 0:
                dict_col_metadata_availbility["int_num_entries_available"] += len(
                    l_int_entry_that_needs_fetching
                )  # update the number of entries available

                # fetch data according to the modes of current zdf
                if self.is_mask and self.is_combined:
                    pass
                elif self.is_mask:
                    za_source.open(
                        path_column_source, mode="r"
                    )  # open source zarr object
                    # open sink zarr object
                    if not zarr_exists(path_column_sink):
                        za_sink.open(
                            path_column_sink,
                            mode="a",
                            shape=za_source.shape,
                            chunks=za_source.chunks,
                            fill_value=za_source.fill_value,
                            dtype=str
                            if za_source.dtype is np.dtype("O")
                            else za_source.dtype,
                        )
                        za_sink.set_attrs(
                            flag_is_being_lazy_loaded=True
                        )  # update metadata of the sink column
                    else:
                        za_sink.open(path_column_sink, mode="a")
                    # fetch and save fetched data to the output column
                    za_sink.set_orthogonal_selection(
                        l_int_entry_that_needs_fetching,
                        za_source.get_orthogonal_selection(
                            l_int_entry_that_needs_fetching
                        ),
                    )  # update sink column values from values using the source ZarrDataFrame
                elif self.is_combined:
                    # %% COMBINED MODE %%
                    # iterate over components
                    # initialize mask
                    if (
                        self.is_interleaved
                        and flag_retrieve_from_all_interleaved_components
                    ):
                        ba_retrieved = bitarray(self._n_rows_unfiltered)
                        ba_retrieved.setall(0)
                    for (
                        int_index_component,
                        zdf,
                        dict_index_mapping_from_combined_to_component,
                        path_column_source,
                    ) in zip(
                        np.arange(len(self._l_zdf)),
                        self._l_zdf,
                        self._l_dict_index_mapping_from_combined_to_component,
                        l_path_column_source,
                    ):
                        # when combined mode is interleaved and only single component is used as a data source, retrieve data from a single component
                        if (
                            self.is_interleaved
                            and not flag_retrieve_from_all_interleaved_components
                            and int_index_component
                            != self.index_zdf_data_source_when_interleaved
                        ):
                            continue
                        # if source column does not exist, continue
                        if path_column_source is None:
                            continue

                        # initialize 'path_column_sink'
                        if flag_mode_internal:  # internal mode
                            # initialize the 'name_col_sink' column of the current zdf object using the column from the current component zdf
                            self.initialize_column(
                                name_col=name_col_sink,
                                zdf_template=zdf,
                                name_col_template=name_col_sink,
                            )
                            za_sink.open(path_column_sink, mode="a")
                            za_sink.set_attrs(
                                flag_is_being_lazy_loaded=True
                            )  # update metadata of the sink column
                        else:  # external mode
                            za_source.open(
                                path_column_source, mode="r"
                            )  # open source zarr object
                            if not zarr_exists(path_column_sink):
                                dtype = (
                                    str
                                    if za_source.dtype is np.dtype("O")
                                    else za_source.dtype
                                )  # retrieve dtype
                                chunks_not_primary_axis = list(
                                    za_source.chunks[1:]
                                )  # retrieve 'chunks_not_primary_axis'
                                za_sink.open(
                                    path_column_sink,
                                    mode="a",
                                    shape=tuple(
                                        [self._n_rows_unfiltered]
                                        + list(za_source.shape[1:])
                                    ),
                                    chunks=tuple(
                                        [
                                            self.get_int_num_rows_in_a_chunk(
                                                dtype,
                                                chunks_not_primary_axis=chunks_not_primary_axis,
                                            )
                                        ]
                                        + chunks_not_primary_axis
                                    ),
                                    fill_value=za_source.fill_value,
                                    dtype=dtype,
                                )
                                za_sink.set_attrs(
                                    flag_is_being_lazy_loaded=True
                                )  # update metadata of the sink column
                            else:
                                za_sink.open(
                                    path_column_sink, mode="a"
                                )  # open sink zarr object

                        # retrieve coordinates of the component zdf
                        l_int_entry_combined, l_int_entry_component = (
                            [],
                            [],
                        )  # initialize the array
                        for int_entry_combined in l_int_entry_that_needs_fetching:
                            if (
                                int_entry_combined
                                in dict_index_mapping_from_combined_to_component
                            ):  # if the entry exist in the source column
                                if (
                                    self.is_interleaved
                                    and flag_retrieve_from_all_interleaved_components
                                ):
                                    if not ba_retrieved[
                                        int_entry_combined
                                    ]:  # if value for the current entry was not retrieved
                                        ba_retrieved[
                                            int_entry_combined
                                        ] = 1  # update the flag
                                        l_int_entry_combined.append(int_entry_combined)
                                        l_int_entry_component.append(
                                            dict_index_mapping_from_combined_to_component[
                                                int_entry_combined
                                            ]
                                        )
                                else:
                                    l_int_entry_combined.append(int_entry_combined)
                                    l_int_entry_component.append(
                                        dict_index_mapping_from_combined_to_component[
                                            int_entry_combined
                                        ]
                                    )

                        # update sink column if there is valid entries to retrieve data and update
                        if len(l_int_entry_combined) > 0:
                            if flag_mode_internal:
                                self[name_col_sink, l_int_entry_combined] = zdf[
                                    name_col_sink, l_int_entry_component
                                ]  # transfer data from the source zdf to the combined column of the current zdf for the current batch
                            else:
                                za_sink.set_orthogonal_selection(
                                    l_int_entry_combined,
                                    za_source.get_orthogonal_selection(
                                        l_int_entry_component
                                    ),
                                )  # update sink column values from values using the source ZarrDataFrame
                        del l_int_entry_combined, l_int_entry_component
                # update availability
                if (
                    not flag_will_be_fully_loaded
                ):  # if the column will be fully loaded, do not update the availability column
                    self[
                        name_col_availability, l_int_entry_that_needs_fetching
                    ] = True  # update availability
            else:
                za_sink.open(path_column_sink, mode="a")  # open sink zarr object

        # update availability column
        # when all entries were loaded, delete the availbility column and modify the sink column metadata
        if (
            dict_col_metadata_availbility["int_num_entries_available"]
            == self._n_rows_unfiltered
        ):
            del self[name_col_availability]  # delete the column
            # update metadata of the sink column
            za_sink.open(path_column_sink, mode="a")
            za_sink.set_attrs(flag_is_being_lazy_loaded=False)
        else:
            # save metadata of availability column
            self.set_column_metadata(
                name_col_availability, dict_col_metadata_availbility
            )  # save metadata

    def get_integer_indices(self, queries=None):
        """# 2022-09-11 21:44:43
        retrieve integer indices from advanced indexing queries.

        queries # slice, list of integer indices, bitarray, numpy arrays (boolean) are one of the possible queries
        """
        # check coordinate arrays
        if isinstance(
            queries, tuple
        ):  # if a tuple is given as queries, assumes it contains a list of coordinate arrays
            queries = queries[0]  # retrieve coordinates in the first axis
        elif isinstance(queries, slice):  # if a slice object has been given
            queries = range(
                *queries.indices(self._n_rows_unfiltered)
            )  # convert slice to range
        else:
            # detect boolean mask
            flag_queries_in_bool_mask = BA.detect_boolean_mask(queries)
            # convert boolean masks to np.ndarray object
            if flag_queries_in_bool_mask:
                if not isinstance(queries, bitarray):  # if type is not bitarray
                    # handle list of boolean values
                    if not isinstance(queries, np.ndarray):
                        queries = np.array(queries, dtype=bool)  # change to ndarray
                    # handle np.ndarray
                    if isinstance(queries, np.ndarray) and queries.dtype != bool:
                        queries = queries.astype(bool)  # change to ndarray
                    queries = BA.to_bitarray(
                        queries
                    )  # convert numpy boolean array to bitarray
                queries = BA.find(queries)  # convert bitarray to generator
        return (
            iter(queries) if hasattr(queries, "__iter__") else queries
        )  # iterate over integer indices

        #         if self._mask is not None : # if mask is available, return the result of the mask (assuming mask is more accessible, possibly available in the local storage)
        #             return self._mask.get_integer_indices( queries )

        #         # if the 'index' column is available in the columns, perform query using zarr module and return the result
        #         if '__index__' in self.columns_excluding_components :
        #             return self[ '__index__', queries ] # return integer indices of the queries

        #         # write the 'index' column
        #         self.initialize_column( '__index__', dtype = int ) # initialize the index column
        #         int_pos = 0
        #         while int_pos < self._n_rows_unfiltered :
        #             int_pos_end_batch = min( int_pos + self.int_num_rows_in_a_chunk, self._n_rows_unfiltered ) # retrieve end coordinate of the current batch
        #             self[ '__index__', int_pos : int_pos_end_batch ] = np.arange( int_pos, int_pos_end_batch ) # write the integer indices
        #             int_pos += self.int_num_rows_in_a_chunk # update 'int_pos'
        #         if self.verbose :
        #             logger.info( f'[ZarrDataFrame] a column for quering integer indices was written' )
        return self["__index__", queries]  # return integer indices of the queries

    def initialize_column(
        self,
        name_col: Union[None, str] = None,
        dtype=np.float64,
        shape_not_primary_axis=(),
        chunks=(),
        categorical_values=None,
        fill_value=0,
        dict_col_metadata: Union[dict, None] = None,
        dict_metadata_description: dict = dict(),
        zdf_template=None,
        name_col_template: Union[str, None] = None,
        path_col_template: Union[str, None] = None,
        flag_rechunk_primary_axis: bool = False,
        flag_dry_run: bool = False,
        data_for_initialization: Union[None, dict] = None,
    ):
        """# 2023-04-20 01:14:04
        initialize columns with a given shape and given dtype
        name_col : Union[ None, str ] = None # name of the column to initialize. if None is given, return the required data for initializing a column
        'dtype' : initialize the column with this 'dtype'
        'shape_not_primary_axis' : initialize the column with this shape excluding the dimension of the primary axis. if an empty tuple or None is given, a 1D array will be initialized.
                for example, for ZDF with length 100,
                'shape_not_primary_axis' = ( ) will lead to creation of zarr object of (100,)
                'shape_not_primary_axis' = ( 10, 10 ) will lead to creation of zarr object of (100, 10, 10)

        'chunks' : chunk size of the zarr object. length of the chunk along the primary axis can be skipped, which will be replaced by 'int_num_rows_in_a_chunk' calculated from 'int_num_bytes_in_a_chunk'  attribute
        'categorical_values' : if 'categorical_values' has been given, set the column as a column containing categorical data
        'fill_value' : fill value of zarr object
        dict_col_metadata : Union[ dict, None ] = None, # a 'dict_col_metadata' of the output ZarrDataFrame column. settings from the given 'dict_col_metadata' will be override other arguments used to construct 'dict_col_metadata', including 'dict_metadata_description' and 'categorical_values'
        dict_metadata_description : dict = dict( ) # the dictionary containing metadata of the column with the following schema:
                    'description' : a brief description of the column
                    'authors' : a list of authors and contributors for the column

        'zdf_template' : zdf object from which to search 'name_col_template' column. by default,
        'name_col_template' : the name of the column to use as a template. if given, 'path_col_template' will be ignored, and use the column as a template to initialize the current column. the column will be searched in the following order: main zdf object --> mask zdf object --> component zdf objects, in the order specified in the list.
        'path_col_template' : the (remote) path to the column to be used as a template. if given, the metadata available in the path will be used to initialize the current column
        flag_rechunk_primary_axis : bool = False, # if True, set the chunk size along the primary axis based on the current 'int_num_bytes_in_a_chunk'
        flag_dry_run : bool : False, # if True, does not initialize the column. instead, only return the data required for initializing the column.
        data_for_initialization : Union[ None, dict ] = None, # use 'data_for_initialization' to initialize a column. all other arguments other than 'name_col' will be overridden.

        === returns ===
        dict_data_for_initialization : data required for initializing the column.
        """
        # retrieve a ZarrServer object
        za = self._zs

        # parse 'data_for_initialization'
        if data_for_initialization is not None:
            # override existing arguments using values from 'data_for_initialization'
            shape_not_primary_axis = data_for_initialization["shape_not_primary_axis"]
            chunks = data_for_initialization["chunks"]
            dtype = data_for_initialization["dtype"]
            fill_value = data_for_initialization["fill_value"]
            dict_col_metadata = data_for_initialization["dict_col_metadata"]

        # hand over to mask if mask is available
        if (
            self._mask is not None
        ):  # if mask is available, save new data to the mask # overwriting on the mask
            self._mask.initialize_column(
                name_col=name_col,
                dtype=dtype,
                shape_not_primary_axis=shape_not_primary_axis,
                chunks=chunks,
                categorical_values=categorical_values,
                fill_value=fill_value,
                zdf_template=zdf_template,
                name_col_template=name_col_template,
                path_col_template=path_col_template,
                flag_rechunk_primary_axis=flag_rechunk_primary_axis,
                flag_dry_run=flag_dry_run,
                data_for_initialization=data_for_initialization,
            )
            return

        if self._n_rows_unfiltered is None:  # if length of zdf has not been set, exit
            return

        if (
            name_col in self.columns_excluding_components
        ):  # if the column exists in the current ZarrDataFrame (excluding component zdf objects), ignore the call and exit
            return

        # if 'name_col' is not given, return the data for initialization
        if name_col is None:
            flag_dry_run = True

        # retrieve metadata information from the template column object
        if not isinstance(
            zdf_template, ZarrDataFrame
        ):  # by default, use self as template zdf object
            zdf_template = self
        if (
            name_col_template is not None and name_col_template in zdf_template
        ):  # use 'name_col_template' as a template if valid name_col has been given
            path_col_template = zdf_template._get_column_path(
                name_col_template
            )  # retrieve path of the template column from the template zdf
        if path_col_template is not None and zarr_exists(
            path_col_template
        ):  # use 'path_col_template' as a template, retrieve settings
            # automatically set arguments based on the template column
            za.open(path_col_template, mode="r")  # open zarr object
            dtype = za.dtype
            shape_not_primary_axis = za.shape[1:]
            chunks = za.chunks
            fill_value = za.fill_value
            # retrieve column metadata
            dict_col_metadata = za.get_attr("dict_col_metadata")
            dict_metadata_description = (
                dict_col_metadata["dict_metadata_description"]
                if "dict_metadata_description" in dict_col_metadata
                else None
            )  # retrieve 'dict_metadata_description' # handle old version of 'dict_col_metadata'
            categorical_values = (
                dict_col_metadata["l_value_unique"]
                if "flag_categorical" in dict_col_metadata
                and dict_col_metadata["flag_categorical"]
                else None
            )  # retrieve categorical values

        # interpret object dtype as the string datatype
        if dtype is np.dtype("O") or dtype == "object":
            dtype = str

        if (
            name_col not in self.columns_excluding_components
        ):  # if the column does not exists in the current ZarrDataFrame (excluding component zdf objects )
            try:
                # check whether the given name_col is valid (invalid column name will raise an error)
                name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve 'name_folder'

                # retrieve path of the column
                path_folder_col = f"{self._path_folder_zdf}{name_folder}/"
                flag_use_locking = (
                    self.use_locking and not flag_dry_run
                )  # if 'flag_dry_run' is True, the column will not be initialized, and locking will not be used.
                if flag_use_locking:  # if locking is used
                    # %% FILE LOCKING %%
                    # if a lock is present, exit the function, since the column has been already initialized
                    if self._zsls.check_lock(f"{path_folder_col}.lock"):
                        if self.verbose:
                            logger.error(
                                f"a lock is present for {path_folder_col} column, indicating that the column has been already initialized by other processes, exiting"
                            )
                        return
                    # acquire the lock before initializing the column
                    flag_lock_acquired = self._zsls.acquire_lock(
                        f"{path_folder_col}.lock"
                    )
                
                """ 
                compose metadata
                """
                if (
                    dict_col_metadata is None
                ):  # if 'dict_col_metadata' is not given, compose the metadata
                    dict_col_metadata = {
                        "flag_categorical": False,
                        "dict_metadata_description": dict_metadata_description,
                    }  # set a default value for 'flag_categorical' metadata attribute # also, add 'dict_metadata_description'
                    dict_col_metadata["flag_filtered"] = (
                        self.filter is not None
                    )  # mark the column containing filtered data

                    # initialize a column containing categorical data
                    if (
                        categorical_values is not None
                    ):  # if 'categorical_values' has been given
                        fill_value = -1  # set fill_value to -1 to represent null values
                        dict_col_metadata[
                            "flag_categorical"
                        ] = True  # set metadata for categorical datatype
                        set_value_unique = set(
                            categorical_values
                        )  # retrieve a set of unique values
                        # handle when np.nan value exist
                        if np.nan in set_value_unique:  # when np.nan value was detected
                            if (
                                "flag_contains_nan" not in dict_col_metadata
                            ):  # update metadata
                                dict_col_metadata[
                                    "flag_contains_nan"
                                ] = True  # mark that the column contains np.nan values
                            set_value_unique.remove(
                                np.nan
                            )  # removes np.nan from the category

                        if "l_value_unique" not in dict_col_metadata:
                            l_value_unique = list(
                                set_value_unique
                            )  # retrieve a list of unique values # can contain mixed types (int, float, str)
                            dict_col_metadata["l_value_unique"] = list(
                                str(e) for e in l_value_unique
                            )  # update metadata # convert entries to string (so that all values with mixed types can be interpreted as strings)
                        else:
                            set_value_unique_previously_set = set(
                                dict_col_metadata["l_value_unique"]
                            )
                            l_value_unique = dict_col_metadata["l_value_unique"] + list(
                                val
                                for val in list(set_value_unique)
                                if val not in set_value_unique_previously_set
                            )  # extend 'l_value_unique'
                            dict_col_metadata[
                                "l_value_unique"
                            ] = l_value_unique  # update metadata

                        # retrieve appropriate datatype for encoding unique categorical values
                        int_min_number_of_bits = (
                            int(np.ceil(math.log2(len(l_value_unique)))) + 1
                        )  # since signed int will be used, an additional bit is required to encode the data
                        if int_min_number_of_bits <= 8:
                            dtype = np.int8
                        elif int_min_number_of_bits <= 16:
                            dtype = np.int16
                        else:
                            dtype = np.int32

                # handle integer dtype
                if (
                    self.flag_store_64bit_integer_as_float
                ):  # if 'flag_store_64bit_integer_as_float' flag is set to True, avoid using np.int64 dtype due to its compatibility with the JavaScript
                    if np.issubdtype(
                        dtype, np.int64
                    ):  # the np.int64 dtype will be saved using the np.float64 dtype
                        dtype = np.float64
                    if (
                        dtype == int
                    ):  # the general 'int' dtype will be saved using the np.int32 dtype
                        dtype = np.int32

                # initialize the zarr objects
                shape = tuple(
                    [self._n_rows_unfiltered] + list(shape_not_primary_axis)
                )  # compose 'shape' of the zarr object
                if flag_rechunk_primary_axis and len(chunks) == len(
                    shape
                ):  # if 'flag_rechunk_primary_axis' is active and the number of dimensions for 'chunks' are the same as that of 'shape', omit the chunk size of the primary axis for re-chunking
                    chunks = chunks[1:]
                chunks = (
                    tuple(chunks)
                    if len(chunks) == len(shape)
                    else tuple(
                        [
                            self.get_int_num_rows_in_a_chunk(
                                dtype, chunks_not_primary_axis=chunks
                            )
                        ]
                        + list(chunks)
                    )
                )  # compose 'chunks' of the zarr object # handle when chunk size for the primary axis was not given
                assert len(chunks) == len(
                    shape
                )  # the length of chunks and shape should be the same

                if (
                    not flag_dry_run
                ):  # initialize the given column # if 'flag_dry_run' is True, does not initialize the column. instead, retrieve data for initialization
                    za.open(
                        path_folder_col,
                        mode="a",
                        shape=shape,
                        chunks=chunks,
                        dtype=dtype,
                        fill_value=fill_value,
                    )  # create a new Zarr object if the object does not exist.

                    # write metadata
                    za.set_attrs(dict_col_metadata=dict_col_metadata)

                    # add column to zdf (and update the associated metadata)
                    self._add_column(name_col, dict_metadata_description)
            finally:
                if flag_use_locking:  # if locking is used
                    # %% FILE LOCKING %%
                    # acquire the lock before initializing the column
                    if flag_lock_acquired:
                        self._zsls.release_lock(f"{path_folder_col}.lock")

            # return data used for initialization
            dict_data_for_initialization = {
                "shape_not_primary_axis": shape[1:],
                "chunks": chunks,
                "dtype": str(dtype),
                "fill_value": fill_value,
                "dict_col_metadata": dict_col_metadata,  # containing required data to initialize a ZarrDataFrame column
            }
            return dict_data_for_initialization

    def __getitem__(self, args):
        """# 2022-12-11 05:45:07
        retrieve data of a column.
        partial read is allowed through indexing (slice/integer index/boolean mask/bitarray is supported)
        if mask is set, retrieve data from the mask if the column is available in the mask.
        also, when the 'flag_use_mask_for_caching' setting is active, use mask for caching data from source data (possibly remote source).

        when combined mode is active, all data of the queried column will be retrieved across the component columns, and saved as a combined column in the current zdf object. Then, the query will be used to retrieve data from the combined column
        """
        """
        # parse arguments
        
        'name_col' : the name of the column
        'coords' : coordinates/slice/mask for the primary axis
        'coords_rest' : coordinates/slices for axis other than the primary axis
        """
        # retrieve a zarr server object
        za = self._zs

        # initialize indexing
        flag_indexing_primary_axis = (
            False  # a boolean flag indicating whether an indexing is active
        )
        flag_coords_in_bool_mask = False
        flag_coords_in_coordinate_arrays = False
        # parse arguments
        if (
            isinstance(args, tuple) and args[1] is not None
        ):  # when indexing on the primary axis is active
            flag_indexing_primary_axis = True  # update the flag
            # parse the args
            if len(args) == 2:
                name_col, coords, coords_rest = args[0], args[1], None
            elif len(args) > 2:
                name_col, coords, coords_rest = args[0], args[1], args[2:]
            # check coordinate arrays
            if isinstance(
                coords, tuple
            ):  # if a tuple is given as coords, assumes it contains a list of coordinate arrays
                flag_coords_in_coordinate_arrays = True
            else:
                # detect boolean mask
                flag_coords_in_bool_mask = BA.detect_boolean_mask(coords)
                # convert boolean masks to np.ndarray object
                if flag_coords_in_bool_mask:
                    # handle np.ndarray mask
                    if isinstance(coords, np.ndarray) and coords.dtype != bool:
                        coords = coords.astype(bool)  # change dtype
                    else:  # handle other masks
                        coords = BA.convert_mask_to_array(coords)
        else:
            # when indexing on the primary axis is not active
            coords = (
                slice(None, None, None)
                if self.filter is None
                else BA.to_array(self.filter)
            )  # retrieve selection filter for the primary axis according to the self.filter
            if isinstance(args, tuple):  # if indexing in non-primary axis is active
                name_col, coords_rest = args[0], args[2:]
            else:  # only column name was given
                name_col, coords_rest = args, None
        flag_indexing_in_non_primary_axis = (
            coords_rest is not None
        )  # a flag indicating indexing in non-primary axis is active

        """
        # retrieve data
        """
        if (
            name_col not in self
        ):  # if name_col is not valid (name_col does not exists in current ZDF, including the mask), exit by returning None
            return None
        name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve the name of the folder
        # load data from mask/combined ZarrDataFrame
        if (
            self._flag_use_lazy_loading
        ):  # use lazy-loading when only partial data will be retrieved
            self.lazy_load(
                coords,
                name_col_sink=name_col,
            )
            # off load to mask
            if self._mask is not None:  # if mask is available
                if (
                    name_col in self._mask
                ):  # if 'name_col' is available in the mask, retrieve data from the mask.
                    return self._mask[args]
        else:  # load an entire column from mask/combined ZarrDataFrame
            # off load to mask
            if self._mask is not None:  # if mask is available
                if (
                    self.flag_use_mask_for_caching and name_col not in self._mask
                ):  # if 'flag_use_mask_for_caching' option is active and the column is not available in the mask, copy the column from the source to the mask
                    zarr_copy(
                        f"{self._path_folder_zdf}{name_folder}/",
                        f"{self._mask._path_folder_zdf}{name_folder}/",
                    )  # copy zarr object from the source to the mask
                    self._mask._add_column(
                        name_col
                    )  # manually add column label to the mask
                if (
                    name_col in self._mask
                ):  # if 'name_col' is available in the mask, retrieve data from the mask.
                    return self._mask[args]
            # collect data from component zdfs and compose a combined column
            if (
                self.is_combined and name_col not in self.columns_excluding_components
            ):  # if data reside only in the component zdf objects, retrieve data from the component objects and save as a column in the current zdf object
                # %% COMBINED MODE %%
                # if the queried column does not exist in the current zdf or mask zdf, fetch data from component zdf objects and save the data to the current zdf or the mask of it
                if self.is_interleaved:
                    # %% COMBINED INTERLEAVED %%
                    zdf = self._l_zdf[
                        self.index_zdf_data_source_when_interleaved
                    ]  # retrieve source zdf
                    dict_index_mapping_interleaved = (
                        self._l_dict_index_mapping_interleaved[
                            self.index_zdf_data_source_when_interleaved
                        ]
                    )  # retrieve index-mapping dictionary of source zdf
                    assert (
                        name_col in zdf
                    )  # the name_col should exist in the zdf object
                    # initialize the 'name_col' column of the current zdf object using the column from the current component zdf
                    self.initialize_column(
                        name_col=name_col, zdf_template=zdf, name_col_template=name_col
                    )

                    # transfer data from the source zdf to the combined column of the current zdf
                    l_int_entry_combined, l_int_entry_component = (
                        [],
                        [],
                    )  # initialize the array
                    for int_entry_combined in dict_index_mapping_interleaved:
                        l_int_entry_combined.append(int_entry_combined)
                        l_int_entry_component.append(
                            dict_index_mapping_interleaved[int_entry_combined]
                        )
                        if (
                            len(l_int_entry_component)
                            >= self.int_max_num_entries_per_batch
                        ):  # if a batch is full, flush the buffer
                            self[name_col, l_int_entry_combined] = zdf[
                                name_col, l_int_entry_component
                            ]  # transfer data from the source zdf to the combined column of the current zdf for the current batch
                            l_int_entry_combined, l_int_entry_component = (
                                [],
                                [],
                            )  # initialize the next batch
                    if (
                        len(l_int_entry_component) >= 0
                    ):  # if the current batch is not empty, flush the buffer
                        self[name_col, l_int_entry_combined] = zdf[
                            name_col, l_int_entry_component
                        ]  # transfer data from the source zdf to the combined column of the current zdf for the current batch
                    del l_int_entry_combined, l_int_entry_component
                else:
                    # %% COMBINED STACKED %%
                    # collect data from stacked czdf
                    int_pos = 0  # initialize the position
                    for zdf in self._l_zdf:
                        if (
                            name_col in zdf
                        ):  # if the 'name_col' exist in the current component zdf
                            # initialize the 'name_col' column of the current zdf object using the column from the current component zdf
                            self.initialize_column(
                                name_col=name_col,
                                zdf_template=zdf,
                                name_col_template=name_col,
                            )

                            # transfer data from component zdf to the combined column of the current zdf object batch by batch
                            st, en = (
                                int_pos,
                                int_pos + zdf._n_rows_unfiltered,
                            )  # retrieve start and end coordinates for the current component

                            int_pos_current_component = 0  # initialize the position of current entry in the current batch
                            while (
                                st + int_pos_current_component < en
                            ):  # until all entries for the current component have been processed
                                # transfer data from component zdf to the combined column of the current zdf object for the current batch
                                self[
                                    name_col,
                                    slice(
                                        st + int_pos_current_component,
                                        min(
                                            en,
                                            st
                                            + int_pos_current_component
                                            + self.int_max_num_entries_per_batch,
                                        ),
                                    ),
                                ] = zdf[
                                    name_col,
                                    slice(
                                        int_pos_current_component,
                                        min(
                                            en - st,
                                            int_pos_current_component
                                            + self.int_max_num_entries_per_batch,
                                        ),
                                    ),
                                ]  # update the combined column using the values retrieved from the current zdf object
                                int_pos_current_component += (
                                    self.int_max_num_entries_per_batch
                                )  # update 'int_pos_current_component' for the next batch
                        int_pos += zdf._n_rows_unfiltered  # update 'int_pos'

        # retrieve data from zdf objects excluding components (current zdf and mask zdf)
        if self.use_locking:  # %% FILE LOCKING %%
            self._zsls.wait_lock(
                f"{self._path_folder_zdf}{name_folder}.lock"
            )  # wait until the lock becomes available (the column is now ready for 'read' operation)

        if name_col in self:  # if name_col is valid
            if (
                name_col in self._loaded_data and not flag_indexing_primary_axis
            ):  # if a loaded data (filtered/unfiltered, according to the self.filter) is available and indexing is not active, return the cached data
                """if (filtered), preloaded data is available"""
                data = self._loaded_data[name_col]  # retrieve memory-cached data
                return (
                    data[:, coords_rest] if flag_indexing_in_non_primary_axis else data
                )  # return a subset of result if 'flag_indexing_in_non_primary_axis' is True
            else:
                """read data from zarr object"""
                # open the zarr object
                za.open(f"{self._path_folder_zdf}{name_folder}/", mode="r")

                if (
                    flag_coords_in_bool_mask
                    and isinstance(coords, np.ndarray)
                    and za.shape == coords.shape
                ):
                    # use mask selection
                    values = za.get_mask_selection(coords)
                elif flag_coords_in_coordinate_arrays:
                    # coordinate array selection
                    values = za.get_coordinate_selection(coords)
                else:
                    # use orthogonal selection as a default
                    values = (
                        za.get_orthogonal_selection(tuple([coords] + list(coords_rest)))
                        if flag_indexing_in_non_primary_axis
                        else za.get_orthogonal_selection(coords)
                    )

                # check whether the current column contains categorical data
                l_value_unique = self.get_categories(
                    name_col
                )  # non-categorical data will get an empty list
                if (
                    len(l_value_unique) == 0
                    or self.flag_retrieve_categorical_data_as_integers
                ):  # handle non-categorical data
                    return values
                else:  # decode categorical data
                    values = values.astype(
                        object
                    )  # prepare data for storing categorical data
                    # perform decoding
                    for t_coord, val in np.ndenumerate(values):
                        values[t_coord] = (
                            l_value_unique[val] if val >= 0 else np.nan
                        )  # convert integer representations to its original string values # -1 (negative integers) encodes np.nan
                    return values

    def __setitem__(self, args, values):
        """# 2023-04-12 17:48:44
        save/update a column at indexed positions.
        when a filter is active, only active entries will be saved/updated automatically.
        boolean mask/integer arrays/slice indexing is supported. However, indexing will be applied to the original column with unfiltered rows (i.e., when indexing is active, filter will be ignored)
        if mask is set, save data to the mask

        automatically detect dtype of the input array/list, including that of categorical data (all string data will be interpreted as categorical data). when the original dtype and dtype inferred from the updated values are different, an error will occur.

        # 2022-08-03 00:32:19 multi-dimensional data 'columns' is now supported. now complex selection approach can be used to set/view values of a given column as shown below
        # 2022-09-04 13:12:17 currently broadcasting is not supported

        zdf[ 'new_col', ( [ 0, 1, 2 ], [ 0, 0, 1 ] ) ] = [ 'three', 'new', 'values' ] # coordinate selection when a TUPLE is given
        zdf[ 'new_col', : 10 ] = np.arange( 1000 ).reshape( ( 10, 100 ) ) # orthogonal selection

        """
        # load additional zarr servers for accessing Zarr objects
        if not hasattr(self, "_zs_sink"):
            self._zs_sink = ZarrServer(None, flag_spawn=self.flag_spawn)
        # retrieve zarr server objects
        za, za_new = self._zs, self._zs_sink

        """
        1) parse arguments
        """
        if self._mode == "r":  # if mode == 'r', ignore __setitem__ method calls
            return

        # initialize indexing
        flag_indexing_primary_axis = (
            False  # a boolean flag indicating whether an indexing is active
        )
        flag_coords_in_bool_mask = False
        flag_coords_in_coordinate_arrays = False
        # parse arguments
        if (
            isinstance(args, tuple) and args[1] is not None
        ):  # when indexing on the primary axis is active
            flag_indexing_primary_axis = True  # update the flag
            # parse the args
            if len(args) == 2:
                name_col, coords, coords_rest = args[0], args[1], None
            elif len(args) > 2:
                name_col, coords, coords_rest = args[0], args[1], args[2:]
            # check coordinate arrays
            if isinstance(
                coords, tuple
            ):  # if a tuple is given as coords, assumes it contains a list of coordinate arrays
                flag_coords_in_coordinate_arrays = True
            else:
                # detect boolean mask
                flag_coords_in_bool_mask = BA.detect_boolean_mask(coords)
                # convert boolean masks to np.ndarray object
                if flag_coords_in_bool_mask:
                    # handle np.ndarray mask
                    if isinstance(coords, np.ndarray) and coords.dtype != bool:
                        coords = coords.astype(bool)  # change dtype
                    else:  # handle other masks
                        coords = BA.convert_mask_to_array(coords)
        else:
            # when indexing on the primary axis is not active
            coords = (
                slice(None, None, None)
                if self.filter is None
                else BA.to_array(self.filter)
            )  # retrieve selection filter for the primary axis according to the self.filter
            if isinstance(args, tuple):  # if indexing in non-primary axis is active
                name_col, coords_rest = args[0], args[2:]
            else:  # only column name was given
                name_col, coords_rest = args, None
        flag_indexing_in_non_primary_axis = (
            coords_rest is not None
        )  # a flag indicating indexing in non-primary axis is active

        # check whether the given name_col contains invalid characters(s), and retrieve the name of the folder where the column will be stored.
        name_folder = self._get_folder_name_from_column_name( name_col )

        """
        2) set data
        """
        # retrieve data from zdf objects excluding components (current zdf and mask zdf)
        # load data from mask/combined ZarrDataFrame
        if (
            self._flag_use_lazy_loading
        ):  # use lazy-loading when only partial data will be retrieved
            # update availability columns
            self.lazy_load(coords, name_col_sink=name_col, flag_mode_write=True)
            # off load to mask for writing new values
            if (
                self._mask is not None
            ):  # if mask is available, save new data to the mask
                if name_col in self._mask:
                    self._mask[args] = values  # set values to the mask
                    return  # exit
        else:
            # if mask is available, save new data/modify existing data to the mask # overwriting on the mask
            if (
                self._mask is not None
            ):  # if mask is available, save new data to the mask
                if (
                    name_col in self and name_col not in self._mask
                ):  # if the 'name_col' exists in the current ZarrDataFrame and not in mask, copy the column to the mask
                    zarr_copy(
                        f"{self._path_folder_zdf}{name_folder}/",
                        f"{self._mask._path_folder_zdf}{name_folder}/",
                    )  # copy zarr object from the source to the mask # ❤️ modify here to be compatible with remote zarr objects/multiprocessing
                    self._mask._add_column(
                        name_col
                    )  # manually add column label to the mask
                self._mask[args] = values  # set values to the mask
                return  # exit

        if (
            self._flag_is_read_only
        ):  # if current store is read-only (and mask is not set), exit
            return  # exit

        """
        retrieve metadata and infer dtypes
        """
        try:
            if self.use_locking:  # %% FILE LOCKING %%
                path_lock = f"{self._path_folder_zdf}{name_folder}.lock"
                flag_lock_already_acquired = (
                    path_lock in self._zsls.currently_held_locks
                )  # retrieve a flag indicating a lock has been already acquired
                if (
                    not flag_lock_already_acquired
                ):  # acquire lock if it has not been acquired before the operation
                    self._zsls.acquire_lock(path_lock)

            # set default fill_value
            fill_value = 0  # set default fill_value
            # define zarr object directory
            path_folder_col = (
                f"{self._path_folder_zdf}{name_folder}/"  # compose the output folder
            )
            # retrieve/initialize metadata
            flag_col_already_exists = zarr_exists(
                path_folder_col
            )  # retrieve a flag indicating that the column already exists

            """ retrieve/infer shape/dtype """
            flag_update_dict_col_metadata = (
                False  # a flag indicating whether the column metadata should be updated
            )
            if flag_col_already_exists:
                """read settings from the existing columns"""
                za.open(path_folder_col, mode="a")  # open Zarr object
                dict_col_metadata = za.get_attr(
                    "dict_col_metadata"
                )  # load previous written metadata

                # retrieve dtype
                dtype = (
                    str if dict_col_metadata["flag_categorical"] else za.dtype
                )  # dtype of cetegorical data columns should be str
            else:
                dtype = None  # define default dtype
                """ create a metadata of the new column """
                flag_update_dict_col_metadata = (
                    True  # indicate that the column metadata should be updated
                )
                dict_col_metadata = {
                    "flag_categorical": False,
                    "dict_metadata_description": None,
                }  # set a default value for 'flag_categorical' metadata attribute and 'dict_metadata_description' attribute
                dict_col_metadata["flag_filtered"] = (
                    self.filter is not None
                )  # mark the column containing filtered data

                # infer the data type of input values
                # if values is numpy.ndarray, use the dtype of the array
                if isinstance(values, np.ndarray):
                    dtype = values.dtype

                # if values is not numpy.ndarray or the dtype is object datatype, use the type of the data returned by the type( ) python function.
                if not isinstance(values, np.ndarray) or str(dtype) == "object":
                    if isinstance(
                        values, (str, float, int)
                    ):  # if a single value has been given
                        # %% BROADCASTING %%
                        dtype = type(values)
                        self.initialize_column(
                            name_col,
                            dtype=dtype,
                            shape_not_primary_axis=(),
                            chunks=(),
                            categorical_values=[values] if dtype is str else None,
                            fill_value=-1 if dtype is str else 0,
                        )  # initialize the column assuming 1D columns
                    else:  # if a list was given
                        # extract the first entry from the array
                        val = values
                        while hasattr(val, "__iter__") and not isinstance(val, str):
                            val = next(
                                val.__iter__()
                            )  # get the first element of the current array
                        dtype = type(val)

                        if isinstance(
                            val, np.ndarray
                        ):  # check if a list of numpy arrays were given
                            dtype = val.dtype  # use the dtype of the first entry
                        elif (
                            dtype is float and str(val) == "nan"
                        ):  # detect nan values # check whether the array contains strings with np.nan values (make sure array starting with np.nan is not a string array containing np.nan values)
                            for t_coord, val in np.ndenumerate(
                                values
                            ):  # np.ndenumerate can handle nexted lists
                                if type(val) is str:
                                    dtype = str
                                    break
                        elif np.issubdtype(
                            dtype, np.integer
                        ):  # if the first value is integer dtype, check all the values to ensure all the values are of integer dtype
                            for t_coord, val in np.ndenumerate(
                                values
                            ):  # np.ndenumerate can handle nexted lists
                                if np.issubdtype(type(val), np.float):
                                    dtype = float
                                    break

            # update the length of zdf if it has not been set.
            if (
                self._n_rows_unfiltered is None
            ):  # if a valid information about the number of rows is available
                self.update_metadata(
                    {"int_num_rows": len(values)}
                )  # retrieve the length of the primary axis # update metadata

            """ convert data to np.ndarray """
            # detect broadcasting
            flag_broadcasting_active = isinstance(values, (str, float, int))

            # retrieve data values from the 'values'
            if isinstance(values, bitarray):
                values = BA.to_array(
                    values
                )  # retrieve boolean values from the input bitarray
            if isinstance(values, pd.Series):
                values = values.values

            # convert values that is not numpy.ndarray to numpy.ndarray object (for the consistency of the loaded_data)
            if not isinstance(values, np.ndarray) and not flag_broadcasting_active:
                values = np.array(
                    values, dtype=object if dtype is str else dtype
                )  # use 'object' dtype when converting values to a numpy.ndarray object if dtype is 'str'
            # detect nested numpy arrays, array with dtype=object containing another arrays (values returned by pd.DataFrame)
            if (
                not flag_broadcasting_active
                and hasattr(values, "__getitem__")
                and hasattr(values[0], "__iter__")
                and values.ravel().shape[0] == values.shape[0]
            ):
                values = np.array(
                    list(values), dtype=object if dtype is str else dtype
                )  # use 'object' dtype when converting values to a numpy.ndarray object if dtype is 'str' # convert back to list and conver to numpy array to remove the nested structure
            # retrieve shape and chunk sizes of the object
            dim_secondary_inferred = (
                [] if flag_broadcasting_active else list(values.shape)[1:]
            )  # infer dimensions excluding primary axis
            shape_inferred = tuple([self._n_rows_unfiltered] + dim_secondary_inferred)
            chunks_inferred = tuple(
                [
                    self.get_int_num_rows_in_a_chunk(
                        dtype, chunks_not_primary_axis=dim_secondary_inferred
                    )
                ]
                + dim_secondary_inferred
            )  # chunk size excluding the primary axis will be same as the shape excluding the primary axis

            # logger.info( shape, chunks, dtype, self._dict_metadata[ 'flag_store_string_as_categorical' ] )
            # write categorical data
            if (
                dtype is str and self._dict_metadata["flag_store_string_as_categorical"]
            ):  # storing categorical data
                # default fill_value for categorical data is -1 (representing np.nan values)
                fill_value = -1
                # update metadata of the column
                if not dict_col_metadata["flag_categorical"]:
                    flag_update_dict_col_metadata = (
                        True  # indicate that the column metadata should be updated
                    )
                    dict_col_metadata[
                        "flag_categorical"
                    ] = True  # set metadata for categorical datatype

                """ retrieve unique values for categorical data """
                if flag_broadcasting_active:
                    set_value_unique = set([values])
                else:
                    set_value_unique = set()
                    mask_nan = pd.isnull(values)  # check np.nan values in the array
                    if (
                        np.sum(mask_nan) > 0
                    ):  # if the array contains np.nan value, add np.nan to the 'set_value_unique'
                        set_value_unique.add(np.nan)
                    # update non-NaN values
                    set_value_unique.update(
                        set(e[1] for e in np.ndenumerate(values[~mask_nan]))
                    )  # handle broadcasting # retrieve a set of unique values in the input array # update values

                # handle when np.nan value exist
                if np.nan in set_value_unique:  # when np.nan value was detected
                    if (
                        "flag_contains_nan" not in dict_col_metadata
                        or not dict_col_metadata["flag_contains_nan"]
                    ):  # update metadata
                        flag_update_dict_col_metadata = (
                            True  # indicate that the column metadata should be updated
                        )
                        dict_col_metadata[
                            "flag_contains_nan"
                        ] = True  # mark that the column contains np.nan values
                    set_value_unique.remove(np.nan)  # removes np.nan from the category

                # compose a list of unique categorical values and save it as a column metadata
                if "l_value_unique" not in dict_col_metadata:
                    flag_update_dict_col_metadata = (
                        True  # indicate that the column metadata should be updated
                    )
                    l_value_unique = list(
                        set_value_unique
                    )  # retrieve a list of unique values # can contain mixed types (int, float, str)
                    dict_col_metadata[
                        "l_value_unique"
                    ] = l_value_unique  # update metadata
                else:  # update existing categories
                    l_value_unique = dict_col_metadata[
                        "l_value_unique"
                    ]  # retrieve 'l_value_unique'
                    set_value_unique_previously_set = set(l_value_unique)
                    l_value_unique_newly_added = list(
                        val
                        for val in list(set_value_unique)
                        if val not in set_value_unique_previously_set
                    )  # retrieve list of new categories
                    if len(l_value_unique_newly_added) > 0:
                        flag_update_dict_col_metadata = (
                            True  # indicate that the column metadata should be updated
                        )
                        l_value_unique = (
                            dict_col_metadata["l_value_unique"]
                            + l_value_unique_newly_added
                        )  # extend 'l_value_unique'
                        dict_col_metadata[
                            "l_value_unique"
                        ] = l_value_unique  # update metadata

                # retrieve appropriate datatype for encoding unique categorical values
                int_min_number_of_bits = (
                    int(np.ceil(math.log2(len(l_value_unique)))) + 1
                )  # since signed int will be used, an additional bit is required to encode the data
                if int_min_number_of_bits <= 8:
                    dtype = np.int8
                elif int_min_number_of_bits <= 16:
                    dtype = np.int16
                else:
                    dtype = np.int32

                def __replace_chunk_size_for_the_primary_axis(
                    chunks, chunk_size_primary_axis
                ):
                    """
                    replace the chunk size for the primary axis of the given chunks
                    """
                    chunks = list(chunks)
                    chunks[0] = chunk_size_primary_axis
                    chunks = tuple(chunks)
                    return chunks

                # retrieve 'int_num_rows_in_a_chunk' using the updated dtype
                int_num_rows_in_a_chunk = self.get_int_num_rows_in_a_chunk(
                    dtype, chunks_not_primary_axis=dim_secondary_inferred
                )
                chunks_inferred = __replace_chunk_size_for_the_primary_axis(
                    chunks_inferred, int_num_rows_in_a_chunk
                )  # update 'chunks_inferred' using the new 'int_num_rows_in_a_chunk'

                # open Zarr object representing the current column
                za.open(
                    path_folder_col, mode="a"
                ) if flag_col_already_exists else za.open(
                    path_folder_col,
                    mode="w",
                    shape=shape_inferred,
                    chunks=chunks_inferred,
                    dtype=dtype,
                    fill_value=fill_value,
                )  # create a new Zarr object if the object does not exist.

                # if dtype changed from the previous zarr object, re-write the entire Zarr object with changed dtype. (this will happens very rarely, and will not significantly affect the performance)
                if (
                    dtype != za.dtype
                ):  # dtype should be larger than za.dtype if they are not equal (due to increased number of bits required to encode categorical data)
                    if self.verbose:
                        logger.info(
                            f"[categorical data] {za.dtype} will be changed to {dtype}"
                        )
                    path_folder_col_new = f"{self._path_folder_zdf}{name_folder}.{bk.UUID( )[ : 4 ]}"  # compose the new output folder
                    za_new.open(
                        path_folder_col_new,
                        mode="w",
                        shape=za.shape,
                        chunks=__replace_chunk_size_for_the_primary_axis(
                            za.chunks, int_num_rows_in_a_chunk
                        ),
                        dtype=dtype,
                    )  # create a new Zarr object using the new dtype # use the new 'int_num_rows_in_a_chunk' from the new dtype
                    za_new[:] = za[:]  # copy the data
                    self.fs.filesystem_operations(
                        "rm", path_folder_col
                    )  # delete the previous Zarr object
                    self.fs.filesystem_operations(
                        "mv", path_folder_col_new, path_folder_col
                    )  # replace the previous Zarr object with the new object
                    za.open(
                        path_folder_col, mode="a", reload=True
                    )  # re-open the new Zarr object

                # encode data
                dict_encode_category = dict(
                    (e, i) for i, e in enumerate(l_value_unique)
                )  # retrieve a dictionary encoding value to integer representation of the value

                if flag_broadcasting_active:
                    # perform encoding for single input value
                    values = (
                        dict_encode_category[values]
                        if values in dict_encode_category
                        else -1
                    )
                else:
                    # perform encoding for multiple values
                    values_before_encoding = values
                    values = np.zeros_like(
                        values_before_encoding, dtype=dtype
                    )  # initialize encoded values
                    for t_coord, val in np.ndenumerate(
                        values_before_encoding
                    ):  # np.ndarray object can be encoded.
                        values[t_coord] = (
                            dict_encode_category[val]
                            if val in dict_encode_category
                            else -1
                        )  # encode strings into integer representations # -1 (negative integers) encodes np.nan, which is a fill_value for zarr object containing categorical data
            else:
                # when categorical data is not used, modify retrieved/inferred dtype (for compatibility with JavaScript implementation of Zarr.js)
                if (
                    self.flag_store_64bit_integer_as_float
                ):  # if 'flag_store_64bit_integer_as_float' flag is set to True, avoid using np.int64 dtype due to its compatibility with the JavaScript
                    if np.issubdtype(
                        dtype, np.int64
                    ):  # the np.int64 dtype will be saved using the np.float64 dtype
                        dtype = np.float64
                    if (
                        dtype == int
                    ):  # the general 'int' dtype will be saved using the np.int32 dtype
                        dtype = np.int32

            # open zarr object and write data
            za.open(path_folder_col, mode="a") if flag_col_already_exists else za.open(
                path_folder_col,
                mode="w",
                shape=shape_inferred,
                chunks=chunks_inferred,
                dtype=dtype,
                fill_value=fill_value,
            )  # create a new Zarr object if the object does not exist.

            if (
                flag_coords_in_bool_mask
                and isinstance(coords, np.ndarray)
                and za.shape == coords.shape
            ):
                # use mask selection
                za.set_mask_selection(coords, values)
            elif flag_coords_in_coordinate_arrays:
                # coordinate array selection
                za.set_coordinate_selection(coords, values)
            else:
                # use orthogonal selection as a default
                za.set_orthogonal_selection(
                    tuple([coords] + list(coords_rest)), values
                ) if flag_indexing_in_non_primary_axis else za.set_orthogonal_selection(
                    coords, values
                )
            # save/update column metadata
            if flag_update_dict_col_metadata:
                za.set_attrs(dict_col_metadata=dict_col_metadata)

            # update metadata of the current zdf object
            if name_col not in self._dict_metadata["columns"]:
                self._add_column(
                    name_col=name_col,
                    dict_metadata_description=dict_col_metadata[
                        "dict_metadata_description"
                    ],
                )  # add 'dict_metadata_description'

            # if indexing was used to partially update the data, remove the cache, because it can cause inconsistency
            if flag_indexing_primary_axis and name_col in self._loaded_data:
                del self._loaded_data[name_col]
            # add data to the loaded data dictionary (object cache) if 'self._flag_load_data_after_adding_new_column' is True and indexing was not used
            if (
                self._flag_load_data_after_adding_new_column
                and not flag_indexing_primary_axis
                and coords_rest is None
                and not flag_broadcasting_active
            ):  # no indexing through secondary axis, too # broadcasting should not been used for caching
                self._loaded_data[name_col] = (
                    values_before_encoding
                    if dict_col_metadata["flag_categorical"]
                    else values
                )
        finally:
            if self.use_locking:  # %% FILE LOCKING %%
                if (
                    not flag_lock_already_acquired
                ):  # release lock if it has not been acquired before the operation
                    self._zsls.release_lock(path_lock)

    def __delitem__(self, name_col: str):
        """# 2023-04-20 17:35:40
        remove the column from the memory and the object on disk
        if mask is set, delete the column of the mask, and does not delete columns of the original ZarrDataFrame
        """
        if self._mode == "r":  # if mode == 'r', ignore __delitem__ method calls
            return  # exit

        # if mask is available, delete the column from the mask
        if self._mask is not None:  # if mask is available
            if (
                name_col in self._mask
            ):  # if the 'name_col' exists in the mask ZarrDataFrame
                del self._mask[name_col]  # delete the column from the mask
            return  # exit

        if (
            self._flag_is_read_only
        ):  # if current store is read-only (and mask is not set), exit
            return  # exit

        if name_col in self:  # if the given name_col is valid
            # remove column from the memory
            self.unload(name_col)
            # remove the column from metadata
            self.update_metadata(l_name_col_to_be_deleted=[name_col])  # update metadata
            # delete the column from the disk ZarrDataFrame object

            path_prefix_col = (
                f"{self._path_folder_zdf}{self._get_folder_name_from_column_name( name_col )}"  # define prefix for column
            )
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.wait_lock(
                    f"{path_prefix_col}.lock"
                )  # wait until the lock becomes available (the column is now ready for 'delete' operation)
            if self.fs.filesystem_operations(
                "exists", path_prefix_col + "/"
            ):  # delete the folder if the folder exists
                self.fs.filesystem_operations("rm", path_prefix_col + "/")

    def __repr__(self):
        """# 2022-07-20 23:00:15"""
        return (
            f"<ZarrDataFrame object{'' if self._n_rows_unfiltered is None else ' containing '}{'' if self.filter is None else f'{self.n_rows}/'}{'' if self._n_rows_unfiltered is None else f'{self._n_rows_unfiltered} rows'} stored at {self._path_folder_zdf}\n\twith the following columns: {sorted( self._dict_metadata[ 'columns' ] )}"
            + (
                "\n\t[combined]-"
                + ("(interleaved)" if self.is_interleaved else "(stacked)")
                + f" ZarrDataFrame, composed of the following ZarrDataFrame objects:\n["
                + "\n".join(str(zdf) for zdf in self._l_zdf)
                + "]"
                if self.is_combined
                else ""
            )
            + ">"
        )

    @property
    def df(self):
        """# 2022-07-01 22:32:00
        return loaded data as a dataframe, with properly indexed rows
        """
        arr_index = (
            np.arange(self._n_rows_unfiltered)
            if self.filter is None
            else BA.to_integer_indices(self.filter)
        )  # retrieve integer indices of the rows
        if len(self._loaded_data) > 0:  # if a cache is not empty
            df = pd.DataFrame(self._loaded_data)
            df.index = arr_index  # add integer indices of the rows
        else:
            df = pd.DataFrame(
                index=arr_index
            )  # build an empty dataframe using the integer indices
        return df

    def update(
        self,
        df,
        flag_use_index_as_integer_indices: bool = True,
        dict_name_col_to_metadata_description: Union[None, dict] = None,
    ):
        """# 2023-03-31 17:14:56
        update ZarrDataFrame with the given 'df'

        df : a DataFrame to update
        flag_use_index_as_integer_indices : bool = True # use index as integer indices. if False, assumes all currently active entries will be updated.
        dict_name_col_to_metadata_description : Union[ None, dict ] = None #
        """
        # retrieve coordinates for partial
        coords = (
            df.index.values
            if flag_use_index_as_integer_indices
            else slice(None, None, None)
        )

        # update each column parallelly
        l_name_col = df.columns.values

        # before dispatching works across processes, add columns to the metadata beforehand in order to avoid race conditions to edit the metadata.
        for name_col in l_name_col:
            self._add_column(
                name_col,
                dict_name_col_to_metadata_description[name_col]
                if isinstance(dict_name_col_to_metadata_description, dict)
                and name_col in dict_name_col_to_metadata_description
                else None,
            )

        def __work(pipe_receiver, pipe_sender):
            """# 2023-01-20 13:10:40"""
            zdf = self.get_fork_safe_version()  # get the fork-safe version
            while True:
                ins = pipe_receiver.recv()
                if ins is None:
                    break
                name_col, values = ins  # parse 'ins'
                self[name_col, coords] = values  # update values
                pipe_sender.send(True)
            zdf.terminate_spawned_processes()  # terminate the servers

        # paralleize work for each column
        bk.Multiprocessing_Batch_Generator_and_Workers(
            gen_batch=zip(l_name_col, (df[name_col].values for name_col in l_name_col)),
            process_batch=__work,
            int_num_threads=self.int_num_cpus,
        )
        self.metadata  # retrieve the latest metadata of the current object

    def load(self, *l_name_col):
        """# 2022-06-20 22:09:42
        load given column(s) into the memory
        """
        for name_col in l_name_col:
            if name_col not in self:  # skip invalid column
                continue
            if name_col not in self._loaded_data:  # if the data has not been loaded
                self._loaded_data[name_col] = self[name_col]

    def unload(self, *l_name_col):
        """# 2022-06-20 22:09:37
        remove the column from the memory.
        if no column names were given, unload an entire cache
        """
        # if no column names were given, unload an entire cache
        if len(l_name_col) == 0:
            self._loaded_data = dict()
        # if more than one column name was given, unload data of a subset of cache
        for name_col in l_name_col:
            if name_col not in self:  # skip invalid column
                continue
            if name_col in self._loaded_data:
                del self._loaded_data[name_col]

    def delete(self, *l_name_col):
        """# 2022-06-20 22:09:31
        remove the column from the memory and from the disk
        """
        for name_col in l_name_col:
            if name_col not in self:  # skip invalid column
                continue
            del self[name_col]  # delete element from the current object

    def get_df(self, *l_name_col):
        """# 2022-11-15 02:41:53
        get dataframe of a given list of columns, and empty the cache
        """
        l_name_col = list(
            e for e in l_name_col if isinstance(e, str) and e in self
        )  # validate 'l_name_col' # use only hashable strings

        # initialize dataframe using the index (integer representations of all entries or entries of the active entries of the filter only)
        df = pd.DataFrame(
            index=np.arange(self._n_rows_unfiltered, dtype=int)
            if self.filter is None
            else BA.to_integer_indices(self.filter)
        )

        if (
            len(l_name_col) == 0
        ):  # if no columns have been given, return en empty dataframe containing only the index
            return df

        # retrieve data
        for name_col in l_name_col:  # for each column
            # retrieve values for the column
            arr = self[name_col]
            if self.get_column_metadata(name_col)[
                "flag_categorical"
            ]:  # if the column contains the categorical data, convert to categorical datatype
                arr = pd.arrays.Categorical(
                    arr
                )  # convert to the array with categorical data type
            # set values to the dataframe
            df[name_col] = arr

        return df

    def get_shape(self, name_col: str):
        """# 2022-08-07 16:01:12
        return the shape of the given column except for the dimension along the primary axis.
        """
        # retrieve zarr server object
        za = self._zs

        # the column should exist
        if name_col not in self:
            if self.verbose:
                logger.info(
                    f"{name_col} not available in the current ZarrDataFrame, exiting"
                )
            return

        if self._mask is not None:  # if mask is available
            if name_col in self._mask:  # if the column is available in the mask
                return self._mask.get_shape(
                    name_col
                )  # return the result of the mask object

        # open a zarr object, and access the shape
        path_folder_zarr = f"{self._path_folder_zdf}{self._get_folder_name_from_column_name( name_col )}/"
        za.open(path_folder_zarr, mode="r")
        return za.shape[
            1:
        ]  # return the shape including the dimension of the primary axis

    def copy_column(
        self,
        name_col_src: str,
        name_col_dst: str,
        zdf_dst=None,
        int_num_rows_in_a_chunk: Union[None, int] = 10000,
    ):
        """# 2023-02-16 20:24:58
        create a copy of a column

        name_col_src : str, # name of the source column
        name_col_dst : str, # name of the destination column
        zdf_dst = None, # destination ZarrDataFrame. if None is given, current ZarrDataFrame object will be the destination.
        int_num_rows_in_a_chunk : Union[ None, int ] = 10000 # the number of rows in a chunk that will be copied to the destination for each batch. if None is given, the column will be copied in a single batch
        """
        # by default, current ZarrDataFrame object will be the destination zdf.
        if zdf_dst is None:
            zdf_dst = self

        # check validity of 'name_col_src' and 'name_col_dst'
        if name_col_src not in self.columns_excluding_components:
            if self.verbose:
                logger.error(
                    f"{name_col_src} does not exist in the source (current) ZarrDataFrame (excluding components), exiting."
                )
            return
        if name_col_dst in zdf_dst.columns_excluding_components:
            if self.verbose:
                logger.error(
                    f"{name_col_dst} already exists in the destination ZarrDataFrame (excluding components), exiting."
                )
            return

        # copy column
        zdf_dst.initialize_column(
            name_col_dst, zdf_template=self, name_col_template=name_col_src
        )  # initialize the column using the column of the current zdf object

        if int_num_rows_in_a_chunk is None:  # copy the column in a single batch
            zdf_dst[name_col_dst] = self[
                name_col_src
            ]  # copy data (with filter applied)
        else:
            # retrieve filter of the current zdf object
            ba_src = (
                self.all(flag_return_valid_entries_in_the_currently_active_layer=False)
                if self.filter is None
                else self.filter
            )

            ns = dict()  # create a namespace
            ns["int_idx_batch"] = 0  # count the number of batch
            ns["l_idx_dst"] = []  # initialize a namespace
            ns["l_idx_src"] = []

            def __flush():  # flush the batch
                zdf_dst[name_col_dst, ns["l_idx_dst"]] = self[
                    name_col_src, ns["l_idx_src"]
                ]  # fetch and copy a chunk of the data for the current batch
                ns["l_idx_dst"] = []  # initialize the namespace for the next batch
                ns["l_idx_src"] = []
                ns["int_idx_batch"] += 1

            for idx_dst, idx_src in enumerate(BA.find(ba_src)):
                # collect idx_dst and idx_src values
                ns["l_idx_dst"].append(idx_dst)
                ns["l_idx_src"].append(idx_src)
                # flush once a batch is full
                if len(ns["l_idx_src"]) >= int_num_rows_in_a_chunk:
                    __flush()
            # flush remaining entries in a single batch
            if len(ns["l_idx_src"]) > 0:
                __flush()
        if self.verbose:
            logger.info(f"copying '{name_col_src}' to {name_col_dst} column completed")

    def save(self, path_folder_zdf: str, l_name_col: Union[None, list] = None):
        """# 2023-02-18 23:26:23
        save data contained in the ZarrDataFrame object to the new path.
        if a filter is active, filtered ZarrDataFrame will be saved.

        'path_folder_zdf' : the output ZarrDataFrame object
        l_name_col : Union[ None, list ] = None # : the list of names of columns to save. if None is given, copy all columns in the current ZarrDataFrame
        """
        # check validity of the path
        path_folder_zdf = (
            os.path.abspath(path_folder_zdf) + "/"
        )  # retrieve abspath of the output object
        assert (
            self._path_folder_zdf != path_folder_zdf
        )  # the output folder should not be same as the folder of the current ZarrDataFrame

        zdf_dst = ZarrDataFrame(
            path_folder_zdf,
            int_max_num_entries_per_batch=self.int_max_num_entries_per_batch,
            int_num_rows=self.n_rows,
            int_num_bytes_in_a_chunk=self.metadata["int_num_bytes_in_a_chunk"],
            flag_enforce_name_col_with_only_valid_characters=self.metadata[
                "flag_enforce_name_col_with_only_valid_characters"
            ],
            flag_store_string_as_categorical=self.metadata[
                "flag_store_string_as_categorical"
            ],
            flag_retrieve_categorical_data_as_integers=self.flag_retrieve_categorical_data_as_integers,
            flag_load_data_after_adding_new_column=self._flag_load_data_after_adding_new_column,
            flag_use_mask_for_caching=self.flag_use_mask_for_caching,
            verbose=self.verbose,
            flag_use_lazy_loading=self._flag_use_lazy_loading,
        )  # open a new zdf using the same setting as the current ZarrDataFrame

        # handle when 'l_name_col' is None
        if l_name_col is None:
            l_name_col = list(
                self.columns
            )  # if no column name is given, copy all columns in the current ZarrDataFrame to the new ZarrDataFrame

        # exit if an empty list was given as the list of names of the columns to save
        if len(l_name_col) == 0:
            return

        def __work(pipe_receiver, pipe_sender):
            """# 2023-01-20 13:10:40"""
            zdf_dst_fork_safe = (
                zdf_dst.get_fork_safe_version()
            )  # get the fork-safe version
            while True:
                ins = pipe_receiver.recv()
                if ins is None:
                    break
                name_col = ins  # parse 'ins'
                self.copy_column(
                    name_col_src=name_col,
                    name_col_dst=name_col,
                    zdf_dst=zdf_dst_fork_safe,
                )  # copy column by column to the output ZarrDataFrame object
                pipe_sender.send(True)
            zdf_dst_fork_safe.terminate_spawned_processes()  # terminate the servers

        # paralleize work for each column
        set_name_col = set(self.columns).intersection(
            l_name_col
        )  # retrieve a set of name_col to save
        bk.Multiprocessing_Batch_Generator_and_Workers(
            gen_batch=iter(set_name_col),
            process_batch=__work,
            int_num_threads=min(
                self.int_num_cpus, len(set_name_col) + 2
            ),  # use the appropriate number of processes for multiprocessing
        )

    def load_as_dict(
        self,
        *l_name_col,
        float_min_proportion_of_active_rows_for_using_array_as_dict: float = 0.1,
        flag_retrieve_categorical_data_as_integers: bool = False,
    ):
        """# 2023-04-10 00:31:04
        load columns as dictionaries, which is accessible through the self.dict attribute, where keys are integer representation of rows and values are data values

        flag_retrieve_categorical_data_as_integers : bool = False # if True, categorical data will be retrieved as integer. the default setting of the current ZarrDataFrame will be overridden
        'float_min_proportion_of_active_rows_for_using_array_as_dict' : A threshold for the transition from dictionary to array for the conversion of coordinates. empirically, dictionary of the same length takes about ~10 times more memory than the array.
                                                                        By default, when the number of active entries in an axis > 10% (or above any proportion that can set by 'float_min_proportion_of_active_rows_for_using_array_as_dict'), an array representing all rows will be used for the conversion of coordinates.
        """
        set_name_col = set(self.columns).intersection(
            l_name_col
        )  # retrieve a set of valid column names
        if len(set_name_col) == 0:  # exit if there is no valid column names
            return

        # prepare
        flag_retrieve_categorical_data_as_integers_back_up = (
            self.flag_retrieve_categorical_data_as_integers
        )  # retrieve the previous settings
        self.flag_retrieve_categorical_data_as_integers = flag_retrieve_categorical_data_as_integers  # retrieve categorical data as integers to make the retrieving data more efficient

        n = (
            self._n_rows_unfiltered
        )  # retrieve the number of rows in the unfiltered ZarrDataFrame
        arr_index = (
            np.arange(n, dtype=int)
            if self.filter is None
            else BA.to_integer_indices(self.filter)
        )  # retrieve integer indices of the rows
        for name_col in set_name_col:
            if name_col in self.dict:  # ignore columns that were already loaded
                continue
            values = self[name_col]  # retrieve values of the given column
            dict_data = (
                np.zeros(n, dtype=values.dtype)
                if (self.n_rows / n)
                > float_min_proportion_of_active_rows_for_using_array_as_dict
                else dict()
            )  # implement a dictionary using an array if the proportion of active rows of ZarrDataFrame is larger than the given threshold to reduce the memory footprint and increase the efficiency of access
            for int_index_row, val in zip(
                arr_index, values
            ):  # iterate through data values of the active rows
                dict_data[int_index_row] = val
            del values
            self.dict[
                name_col
            ] = dict_data  # add column loaded as a dictionary to the cache

        self.flag_retrieve_categorical_data_as_integers = flag_retrieve_categorical_data_as_integers_back_up  # restore the previous settings

    def get_zarr(self, name_col: str, flag_spawn: Union[None, bool] = None):
        """# 2022-12-05 23:45:38
        get read-only zarr object of a column. return zarr-server with a spawned process (always read fork-safe, regardless of zarr implementation) if current zdf contains remote zdf component or current zdf is remotely located.
        when zarr server is returned, the zarr server should be disabled before being garbage collected, or it will cause runtime error (due to an interrupted interprocess communication)

        flag_spawn : Union[ None, bool ] = None # use a spawned process for zarr operation. by default, use a spawned process for objects stored remotely.
        """
        # handle inputs
        if flag_spawn is None:
            flag_spawn = (
                self.contains_remote
            )  # set default 'flag_spawn'. return zarr server if current zdf contains remote

        # the column should exist
        if name_col not in self:
            if self.verbose:
                logger.info(
                    f"{name_col} not available in the current ZarrDataFrame, exiting"
                )
            return
        
        name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve the name of the folder
        if self._mask is not None:  # if mask is available
            if (
                name_col not in self._mask
            ):  # if the column is not available in the mask, copy the column from the source to the mask
                zarr_copy(
                    f"{self._path_folder_zdf}{name_folder}/",
                    f"{self._mask._path_folder_zdf}{name_folder}/",
                )  # copy zarr object from the source to the mask
                self._mask._add_column(
                    name_col
                )  # manually add column label to the mask
            return self._mask.get_zarr(
                name_col, flag_spawn=flag_spawn
            )  # return the result of the mask object

        # define path
        path_folder_zarr = f"{self._path_folder_zdf}{name_folder}/"

        # open a zarr server
        za = ZarrServer(path_folder_zarr, "r", flag_spawn=flag_spawn)
        return za  # return zarr object

    def get_zarr_with_lock(self, name_col: str):
        """# 2022-08-06 11:29:58
        get multiprocessing-enabled (with filesystem-lock) zarr object of the given column.
        """
        # the column should exist
        if name_col not in self:
            if self.verbose:
                logger.info(
                    f"{name_col} not available in the current ZarrDataFrame, exiting"
                )
            return
        
        name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve the name of the folder
        if self._mask is not None:  # if mask is available
            if (
                name_col not in self._mask
            ):  # if the column is not available in the mask, copy the column from the source to the mask
                zarr_copy(
                    f"{self._path_folder_zdf}{name_folder}/",
                    f"{self._mask._path_folder_zdf}{name_folder}/",
                )  # copy zarr object from the source to the mask
                self._mask._add_column(
                    name_col
                )  # manually add column label to the mask
            return self._mask.get_zarr_with_lock(
                name_col
            )  # return the result of the mask object

        # define pathes
        path_folder_lock = f"{self._path_folder_zdf}{name_folder}.sync/"  # define path to locks for parallel processing with multiple processes
        path_folder_zarr = f"{self._path_folder_zdf}{name_folder}/"

        # if lock already exists, exit
        if self.fs.filesystem_operations("exists", path_folder_lock):
            if self.verbose:
                logger.info(
                    f"current column {name_col} appear to be used in another processes, exiting"
                )
            return None, None

        # if mode == 'r', return read-only object
        if self._mode == "r":

            def __delete_nothing():
                """# 2022-08-06 13:36:10
                place-holding dummy function
                """
                pass

            return (
                zarr.open(path_folder_zarr, "r"),
                __delete_nothing,
            )  # when array is read-only, it is safe to read from multiple processes

        # open a zarr object, write-from-multiple-processes-enabled
        za = zarr.open(
            path_folder_zarr,
            mode="a",
            synchronizer=zarr.ProcessSynchronizer(path_folder_lock),
        )  # use process-sync lock

        def __delete_locks():
            """# 2022-08-06 13:20:57
            destroy the locks used for multiprocessing-enabled modification of a zarr object
            """
            self.fs.filesystem_operations("rm", path_folder_lock)

        return za, __delete_locks

    def rename_column(self, name_col_before: str, name_col_after: str):
        """# 2022-11-15 00:19:15
        rename column of the current ZarrDataFrame
        """
        # exit if currently read-only mode is active
        if self._mode == "r":
            return
        # retrieve up-to-date metadata
        self.metadata
        if (
            name_col_before in self.columns_excluding_components
        ):  # does not rename columns in the component RamData
            # if the column name already exists, return
            if name_col_after in self.columns_excluding_components:
                if self.verbose:
                    logger.info(
                        f"[ZarrDataFrame.rename_column] 'name_col_after' {name_col_after} already exists in the current ZDF, exiting"
                    )
                return
            # if a mask is available, call method on the mask
            if self._mask is not None:  # if mask is available :
                self._mask.rename_column(
                    name_col_before=name_col_before, name_col_after=name_col_after
                )
                return

            # rename folder containing column zarr object
            filesystem_operations(
                "mv",
                f"{self._path_folder_zdf}{self._get_folder_name_from_column_name( name_col_before )}/",
                f"{self._path_folder_zdf}{self._get_folder_name_from_column_name( name_col_after )}/",
            )

            # remove previous column name and add new column name
            self.update_metadata(
                dict_rename_name_col={name_col_before: name_col_after}
            )  # update metadata

    def resize(self, int_num_rows_new: int, flag_avoid_shrinking: bool = True):
        """# 2023-05-06 01:00:54 

        int_num_rows_new : int, # the new number of rows (for resizing zdf)
        flag_avoid_shrinking : bool = True # ignore function call if the number of rows decreases
        """
        # retrieve zarr server object
        za = self._zs

        if (
            self._n_rows_unfiltered == int_num_rows_new
        ):  # ignore when the number of previous and new rows are the same
            return
        if (self._n_rows_unfiltered > int_num_rows_new) and flag_avoid_shrinking:
            return

        # update ZarrDataFrame metadata
        self.update_metadata(
            dict_metadata_to_be_updated={"int_num_rows": int(int_num_rows_new)}
        )

        # resize column
        def _resize_column(name_folder):
            """
            resize a single column
            """
            za.open(f"{self._path_folder_zdf}{name_folder}", mode="a")
            l_shape = list(za.shape)
            l_shape_new = [int_num_rows_new] + l_shape[1:]
            za.resize(*l_shape_new)

        # resize all columns
        for name_col in self.columns:  # for each column
            name_folder = self._get_folder_name_from_column_name( name_col ) # retrieve the name of the folder
            if self._zsls is None:
                _resize_column(name_folder)
            else:
                self._zsls.acquire_lock(
                    f"{self._path_folder_zdf}{name_folder}.lock/"
                )  # acquire lock
                _resize_column(name_folder)
                self._zsls.release_lock(
                    f"{self._path_folder_zdf}{name_folder}.lock/"
                )  # release lock

    def get_categorical_data_as_integers(self, name_col: str):
        """# 2023-03-11 11:02:15
        get categorical values of a given column as integer values

        name_col : str # the name of the column containing categorical data
        flag_use_integer_representation_of_category : bool = False # use integer representation of category
        """
        # handle invalid inputs
        if name_col not in self:
            if self.verbose:
                logger.error(f"name_col '{name_col}' does not exist, exiting")
            raise KeyError(f"name_col '{name_col}' does not exist.")

        # retrieve a list of categories
        l_cat = self.get_categories(name_col)
        if len(l_cat) == 0:
            if self.verbose:
                logger.error(
                    f"categories are not available for the current column '{name_col}', exiting"
                )
            raise KeyError(
                f"categories are not available for the current column '{name_col}', exiting"
            )

        # prepare
        flag_retrieve_categorical_data_as_integers_back_up = (
            self.flag_retrieve_categorical_data_as_integers
        )  # retrieve the previous settings
        self.flag_retrieve_categorical_data_as_integers = True  # retrieve categorical data as integers to make the retrieving data more efficient

        # retrieve labels
        arr_int_cat = self[name_col]  # retrieve categories (in integer format)

        # exit
        self.flag_retrieve_categorical_data_as_integers = flag_retrieve_categorical_data_as_integers_back_up  # restore the previous settings
        return arr_int_cat

    def map_category_to_entries(
        self,
        name_col: str,
        flag_use_integer_representation_of_category: bool = False,
        flag_return_dict_cat_to_num_entries: bool = False,
    ):
        """# 2023-03-12 01:29:33
        retrieve mapping of categories to entries (if a filter is active, only the active entries will be included)

        name_col : str # the name of the column containing categorical data
        flag_use_integer_representation_of_category : bool = False # use integer representation of category
        flag_return_dict_cat_to_num_entries : bool = False # return the number of entries for each category, along with dict_cat_to_l_index
        """
        # retrieve labels
        arr_int_cat = self.get_categorical_data_as_integers(
            name_col=name_col
        )  # retrieve categories (in integer format)
        l_cat = self.get_categories(name_col)
        n = (
            self._n_rows_unfiltered
        )  # retrieve the number of rows in the unfiltered ZarrDataFrame
        arr_index = (
            np.arange(n, dtype=int)
            if self.filter is None
            else BA.to_integer_indices(self.filter)
        )  # retrieve integer indices of the rows

        dict_int_cat_to_l_index = dict()
        for index, int_cat in zip(arr_index, arr_int_cat):
            if int_cat not in dict_int_cat_to_l_index:
                dict_int_cat_to_l_index[int_cat] = list()
            dict_int_cat_to_l_index[int_cat].append(index)

        # convert 'dict_int_cat_to_l_index' to 'dict_cat_to_l_index'
        dict_cat_to_l_index = (
            dict_int_cat_to_l_index
            if flag_use_integer_representation_of_category
            else dict(
                (l_cat[int_cat], dict_int_cat_to_l_index[int_cat])
                for int_cat in dict_int_cat_to_l_index
            )
        )
        del dict_int_cat_to_l_index

        if flag_return_dict_cat_to_num_entries:
            dict_cat_to_num_entries = dict(
                (cat, len(dict_cat_to_l_index[cat])) for cat in dict_cat_to_l_index
            )  # count the number of entries in each category
            return (dict_cat_to_l_index, dict_cat_to_num_entries)
        else:
            return dict_cat_to_l_index

    def count_category(
        self, name_col: str, flag_use_integer_representation_of_category: bool = False
    ):
        """# 2023-04-28 04:04:57
        count the number of entries for each category (if a filter is active, only the active entries will be included)

        name_col : str # the name of the column containing categorical data
        flag_use_integer_representation_of_category : bool = False # use integer representation of category
        """
        # retrieve labels
        arr_int_cat = self.get_categorical_data_as_integers(
            name_col=name_col
        )  # retrieve categories (in integer format)
        arr_int_cat = arr_int_cat[
            arr_int_cat != -1
        ]  # exclude NaN values, encoded by -1 values
        l_cat = self.get_categories(name_col)
        dict_int_cat_to_num_entries = bk.COUNTER(arr_int_cat)  # count labels
        dict_cat_to_num_entries = (
            dict_int_cat_to_num_entries
            if flag_use_integer_representation_of_category
            else dict(
                (l_cat[int_cat], dict_int_cat_to_num_entries[int_cat])
                for int_cat in dict_int_cat_to_num_entries
            )
        )  # change labels
        del dict_int_cat_to_num_entries
        return dict_cat_to_num_entries

    def rechunk_column(self, name_col: str):
        """# 2023-01-19 00:17:28
        rechunk a given column using the current 'int_num_bytes_in_a_chunk' settings.

        name_col : str # the name of the column to rechunk
        """
        # check validity of 'name_col'
        if name_col not in self.columns_excluding_components:
            if self.verbose:
                logger.error(
                    f"{name_col} does not exist in the current ZarrDataFrame (excluding components), exiting."
                )
            return

        name_col_temp = f"{name_col}.{bk.UUID( )[ : 4 ]}"  # retrieve a temporary column name
        self.initialize_column(
            name_col_temp, name_col_template=name_col, flag_rechunk_primary_axis=True
        )  # initialize the column using the column of the current zdf object  # rechunk along the primary axis
        self[name_col_temp, :] = self[name_col, :]  # write all data into the column
        self.delete(name_col)  # delete the original column
        self.rename_column(
            name_col_temp, name_col
        )  # rename the temporary column to the original column name
        if self.verbose:
            logger.info(f"rechunking '{name_col}' column completed")

    def rechunk(self, l_name_col: Union[None, list] = None):
        """# 2023-01-18 23:44:32
        rechunk columns using the current 'int_num_bytes_in_a_chunk' settings.

        l_name_col : Union[ None, list ] = None # : the list of names of columns to rechunk. if None is given, all columns will be rechunked in the current ZarrDataFrame
        """
        # handle when 'l_name_col' is None
        if l_name_col is None:
            l_name_col = list(
                self.columns_excluding_components
            )  # if no column name is given, copy all columns in the current ZarrDataFrame to the new ZarrDataFrame (excluding components)

        def __work(pipe_receiver, pipe_sender):
            """# 2023-01-20 13:10:40"""
            zdf = self.get_fork_safe_version()  # get the fork-safe version
            while True:
                ins = pipe_receiver.recv()
                if ins is None:
                    break
                name_col = ins  # parse 'ins'
                zdf.rechunk_column(name_col)  # rechunk the column
                pipe_sender.send(True)
            zdf.terminate_spawned_processes()  # terminate the servers

        # paralleize work for each column
        bk.Multiprocessing_Batch_Generator_and_Workers(
            gen_batch=iter(
                set(self.columns_excluding_components).intersection(l_name_col)
            ),
            process_batch=__work,
            int_num_threads=self.int_num_cpus,
        )

    def search_columns(self, *args, **kwargs):
        """# 2023-03-05 19:14:17
        search columns of the current object
        """
        return bk.Search_list_of_strings_with_multiple_query(
            list(self.columns), *args, **kwargs
        )

    def lock(self, *l_name_col):
        """# 2023-04-20 17:48:37

        lock a list of columns reside in the current object and return the set of names of the column newly locked.
        """
        if not self.use_locking:  # if lock is not used, exit
            return
        # %% FILE LOCKING %%
        set_name_col_newly_locked = (
            set()
        )  # collect the name of the columns that were newly locked.
        for name_col in l_name_col:  # for each column
            if (
                name_col not in self.columns_excluding_components
            ):  # does not lock the column that are present in the current object.
                continue
            # acquire lock of the column of the lock has not been acquired.
            path_lock = f"{self.path_folder}{self._get_folder_name_from_column_name( name_col )}.lock/"
            if (
                path_lock not in self.locking_server.currently_held_locks
            ):  # acquire lock if it has not been acquired before the operation
                self.locking_server.acquire_lock(path_lock)
                set_name_col_newly_locked.add(
                    name_col
                )  # add the column to the set of name_col with newly acquired locks
        return set_name_col_newly_locked

    def unlock(self, *l_name_col):
        """# 2023-04-20 18:40:53

        release locks of a list of columns reside in the current object and return the set of names of the column whose locks were released.
        """
        if not self.use_locking:  # if lock is not used, exit
            return
        # %% FILE LOCKING %%
        set_name_col_released = (
            set()
        )  # collect the name of the columns that were newly locked.
        for name_col in l_name_col:  # for each column
            if (
                name_col not in self.columns_excluding_components
            ):  # does not lock the column that are present in the current object.
                continue
            # release the lock of the column of the lock has been acquired.
            path_lock = f"{self.path_folder}{self._get_folder_name_from_column_name( name_col )}.lock/"
            if (
                path_lock in self.locking_server.currently_held_locks
            ):  # release the lock if the lock has been acquired by the current object
                self.locking_server.release_lock(path_lock)
                set_name_col_released.add(
                    name_col
                )  # add the column to the set of name_col with newly acquired locks
        return set_name_col_released


""" a class for representing axis of RamData (barcodes/features) """


class IndexMappingDictionary:
    """# 2022-09-02 00:53:27
    a light-weight class for representing dictionary for mapping integer indices

    'int_length_component_axis' : length of the component
    'int_offset' : offset of the start of the component from the start of the combined axis
    'flag_component_to_combined' : set this to True if mapping component to combined axis
    """

    def __init__(
        self,
        int_length_component_axis: int,
        int_offset: int,
        flag_component_to_combined=True,
    ):
        """# 2022-08-30 11:48:50"""
        # set attributes
        self._int_length_component_axis = int_length_component_axis
        self._int_offset = int_offset
        self._flag_component_to_combined = flag_component_to_combined

    def __getitem__(self, int_entry_component):
        """# 2022-08-30 11:57:21
        perform mapping
        """
        return (
            int_entry_component + self._int_offset
            if self._flag_component_to_combined
            else int_entry_component - self._int_offset
        )

    def __contains__(self, e):
        """# 2022-09-02 00:53:20"""
        return (
            0 <= e < self._int_length_component_axis
            if self._flag_component_to_combined
            else 0 + self._int_offset
            <= e
            < self._int_length_component_axis + self._int_offset
        )


class RamDataAxis:
    """# 2023-04-16 21:16:54
    a memory-efficient container of features/barcodes and associated metadata for a given RamData object.

    # 2022-08-29 12:45:51
    Now supports combined axes, which identify combined axes type ('interleaved' or 'stacked') based on the string representations of the entries of each axis.
    For metadata, data will be retrieved across the metadata components of individual axis objects and saved to the current metadata (which can serve as a cache)

    'path_folder' : a folder containing the axis
    'name_axis' : ['barcodes', 'features']
    'int_index_str_rep' : a integer index for the column for the string representation of the axis in the string Zarr object (the object storing strings) of the axis
    'mode' : file mode. 'r' for read-only mode and 'a' for mode allowing modifications
    'path_folder_mask' : a local (local file system) path to the mask of the current Axis that allows modifications to be written without modifying the source. if a valid local path to a mask is given, all modifications will be written to the mask
    'flag_is_read_only' : read-only status of RamData
    int_num_cpus : int = 10, # the number of process for parallel processing of metadata columns

    'dict_kw_zdf' : keworded arguments for ZarrDataFrame instances, which contains metadata. for more details, see ZarrDataFrame class description.

    === arguments controlling batch size ===
    'int_max_num_entries_per_batch' = 1000000 # the maximum number of entries that will be processed as a batch for each (component) axis.

    === settings for combined RamDataAxis object ===
    'l_ax' : a list of RamDataAxis objects that will be combined
    'index_ax_data_source_when_interleaved' : the index of the axis object to retrieve data when combining mode is 'interleaved' (rows shared between axis objects)
    'flag_check_combined_type' = False : Setting this flag to True will run a check whether the given list of axis objects do share common string representations. If each axis contains unique set of string representations,
            the list of axis objects will be treated using 'stacked' option, and RamDataAxis.is_interleaved will show False value. Setting this value to True will consume a lot of memory linearly increasing
            with the number of string representations that should be loaded for checking conditions for 'interleaved' mode.

    'flag_is_interleaved' = False # indicate the type of current 'combined' RamDataAxis, indicating whether to interpret the given list of RamDataAxis object as interleaved (if True) or stacked (if False).
            if True and the current RamDataAxis is in 'combined' mode, an index mapping dictionary will be constructed for each axis.

    'flag_load_all_string_representations_from_components' = False # if True, load all string representations in zarr format AND chunks format (for compatibility with Zarr.js).
        if False, string representations will be loaded as it is accessed. to load string representations in chunks format (lazy-loading not supported), please run RamDataAxis.prepare_javascript_application method.

    === Synchronization across multiple processes ===
    zarrspinlockserver : Union[ None, ZarrSpinLockServer ] = None # a ZarrSpinLockServer object for synchronization of methods of the current object.
    flag_spawn : Union[ None, bool ] = None # by default, automatically determines whether 'spawn' method should be used during multiprocessing. When Zarr objects are located remotely, 'spawn' method will be used.

    """

    def __init__(
        self,
        path_folder: str,
        name_axis: str,
        l_ax: Union[list, tuple, None] = None,
        index_ax_data_source_when_interleaved=0,
        flag_check_combined_type=False,
        flag_is_interleaved: bool = False,
        int_max_num_entries_per_batch=1000000,
        int_num_entries_in_a_chunk=10000,
        ba_filter: Union[bitarray, None] = None,
        ramdata=None,
        int_index_str_rep: int = 0,
        mode: str = "a",
        path_folder_mask: Union[str, None] = None,
        flag_is_read_only: bool = False,
        dict_kw_zdf: dict = {
            "flag_retrieve_categorical_data_as_integers": False,
            "flag_load_data_after_adding_new_column": True,
            "flag_enforce_name_col_with_only_valid_characters": False,
            "int_max_num_entries_per_batch": 1000000,
        },
        dict_kw_view: dict = {
            "float_min_proportion_of_active_entries_in_an_axis_for_using_array": 0.1,
            "dtype": np.int32,
        },
        flag_load_all_string_representations_from_components: bool = False,
        zarrspinlockserver: Union[None, ZarrSpinLockServer] = None,
        flag_spawn: Union[None, bool] = None,
        int_num_cpus: int = 10,
        verbose: bool = True,
    ):
        """# 2022-08-30 12:25:03"""
        # set attributes
        self._int_num_cpus = int_num_cpus
        self._mode = mode
        self._flag_is_read_only = flag_is_read_only
        self._path_folder_mask = path_folder_mask
        self.verbose = verbose
        self._name_axis = name_axis
        self._path_folder = path_folder
        self.int_max_num_entries_per_batch = int_max_num_entries_per_batch
        self.int_num_entries_in_a_chunk = int_num_entries_in_a_chunk
        self.int_index_str_rep = int_index_str_rep  # it can be changed later
        self._ramdata = ramdata  # initialize RamData reference
        # setting for combined RamDataAxis
        self._l_ax = l_ax
        self._index_ax_data_source_when_interleaved = (
            index_ax_data_source_when_interleaved
        )
        self._l_cumulated_len_stacked = None  # a list of cumulated stacked length of entries when current axis is in 'stacked-combined' mode
        self._l_dict_index_mapping_interleaved = None  # set default value for 'self._l_dict_index_mapping_interleaved', which is required for self.is_interleaved function. # similar to 'self._l_dict_index_mapping_from_combined_to_component' but specific to interleaved combined axis object
        self._l_dict_index_mapping_from_combined_to_component = None
        self._l_dict_index_mapping_from_component_to_combined = None  # set default value for list of dictionaries (or similar class) for mapping component indices to combined indices. this will be used for both combined-stacked and combined-interleaved.
        self._dict_index_mapping_from_combined_to_dest_component = (
            None  # set default mapping to destination component
        )
        self._int_index_component_destination = None

        """ set multiprocessing methods """
        if flag_spawn is None:
            flag_spawn = self.is_remote
        self._flag_spawn = flag_spawn

        # load a zarr spin lock server
        self._zsls = (
            zarrspinlockserver
            if isinstance(zarrspinlockserver, ZarrSpinLockServer)
            else None
        )

        # %% COMBINED MODE %%
        if self.is_combined:
            # determines 'combined' type
            """run test for determining combined mode ('interleaved' vs. 'stacked')"""
            if (
                flag_check_combined_type
            ):  # check combined type of the given list of RamDataAxis objects (it might be 'interleaved' or 'stacked')
                # initialize 'flag_is_interleaved'
                flag_is_interleaved = (
                    False  # set 'flag_is_interleaved' to False by default
                )
                # initialize 'interleaved' combined axis type detection
                int_num_entries_encountered = 0
                set_str_rep_encountered = {}
                for ax in self._l_ax:  # for each axis
                    int_pos_component = 0  # initialize position in the component
                    while (
                        int_pos_component < ax.int_num_entries
                    ):  # until all entries of the current component axis have been processed
                        l_str_entry = ax.get_str(
                            slice(
                                int_pos_component,
                                min(
                                    ax.int_num_entries,
                                    int_pos_component
                                    + self.int_max_num_entries_per_batch,
                                ),
                            )
                        )  # retrieve string representations of the current batch
                        int_num_entries_encountered += len(
                            l_str_entry
                        )  # update the number of encountered entries
                        set_str_rep_encountered.update(
                            l_str_entry
                        )  # update currently encountered set of unique string representation

                        # check 'interleaved' type
                        if int_num_entries_encountered != len(
                            set_str_rep_encountered
                        ):  # if entries with duplicated string representation are detected, confirm the 'interleaved' combined axis type
                            flag_is_interleaved = True
                            break

                        int_pos_component += (
                            self.int_max_num_entries_per_batch
                        )  # update 'int_pos_component'

            """ if current 'combined' type is 'interleaved', load/build an index-mapping dictionary """
            if flag_is_interleaved:
                path_folder_interleaved_mapping = f"{path_folder}{name_axis}.interleaved.mapping/"  # define a folder for saving mapping information for 'interleaved' 'combined' axis
                if zarr_exists(
                    path_folder_interleaved_mapping
                ):  # if an output zarr object exists
                    # if folder exists, load index mapping dictionary
                    za = zarr.open(path_folder_interleaved_mapping)
                    # load metadata
                    dict_metadata = za.attrs["dict_metadata"]
                    l_int_num_records = dict_metadata["l_int_num_records"]

                    l_dict_index_mapping_interleaved = (
                        []
                    )  # initialize 'l_dict_index_mapping_interleaved'
                    l_dict_index_mapping_from_component_to_combined = (
                        []
                    )  # initialize 'l_dict_index_mapping_from_component_to_combined'
                    # initialize 'dict_index_mapping_interleaved' for each axis object
                    int_pos = 0
                    for (
                        int_num_records
                    ) in l_int_num_records:  # for each length of axis object
                        arr_int_entry_combined, arr_int_entry_component = za[
                            int_pos : int_pos + int_num_records
                        ].T.astype(
                            int
                        )  # retrieve data
                        int_pos += int_num_records  # update 'int_pos'
                        dict_index_mapping_interleaved = dict(
                            (int_entry_combined, int_entry_component)
                            for int_entry_combined, int_entry_component in zip(
                                arr_int_entry_combined, arr_int_entry_component
                            )
                        )  # initialize the mapping
                        dict_index_mapping_from_component_to_combined = dict(
                            (int_entry_component, int_entry_combined)
                            for int_entry_combined, int_entry_component in zip(
                                arr_int_entry_combined, arr_int_entry_component
                            )
                        )  # initialize the mapping from component to combined axis
                        l_dict_index_mapping_interleaved.append(
                            dict_index_mapping_interleaved
                        )  # add index mapping dictionary
                        l_dict_index_mapping_from_component_to_combined.append(
                            dict_index_mapping_from_component_to_combined
                        )
                        del (
                            dict_index_mapping_interleaved,
                            dict_index_mapping_from_component_to_combined,
                        )
                else:
                    """build a mapping and write string representations of the combined axis"""
                    # if an output zarr object does not exist
                    za = zarr.open(
                        path_folder_interleaved_mapping,
                        "w",
                        dtype=np.float64,
                        shape=(sum(ax.int_num_entries for ax in self._l_ax), 2),
                        chunks=(self.int_max_num_entries_per_batch, 2),
                        fill_value=-1,
                    )

                    # The combined axis will contain automatically de-duplicated entries
                    # Also, during de-duplication, only the unique entries that encountered first will be retained
                    dict_str_entry_to_int_entry = dict()
                    int_entry_new_combined = 0  # new int_entry of the combined axis
                    l_int_num_records = (
                        []
                    )  # the collect the number of mapping records for each axis object
                    int_pos_mapping = 0  # initialize the position of the mapping records for writing files
                    l_dict_index_mapping_interleaved = []
                    l_dict_index_mapping_from_component_to_combined = (
                        []
                    )  # initialize 'l_dict_index_mapping_from_component_to_combined'
                    for ax in self._l_ax:  # for each axis component
                        dict_index_mapping_from_component_to_combined = (
                            dict()
                        )  # initialize the mapping

                        # process string representations of the current axis component object for each batch
                        int_pos_component = 0  # initialize position in the component
                        while (
                            int_pos_component < ax.int_num_entries
                        ):  # until all entries of the current component axis have been processed
                            l_str_entry = ax.get_str(
                                slice(
                                    int_pos_component,
                                    min(
                                        ax.int_num_entries,
                                        int_pos_component
                                        + self.int_max_num_entries_per_batch,
                                    ),
                                )
                            )  # retrieve string representations of the current batch
                            for int_entry, str_entry in enumerate(
                                l_str_entry
                            ):  # for each entry of the current axis
                                int_entry = (
                                    int_entry + int_pos_component
                                )  # retrieve a corrected integer representation of the current entry
                                # add the str_entry to the combined axis (if it does not exist)
                                if str_entry not in dict_str_entry_to_int_entry:
                                    dict_str_entry_to_int_entry[
                                        str_entry
                                    ] = int_entry_new_combined  # add the str_entry to the combined axis
                                    int_entry_new_combined += (
                                        1  # update 'int_entry_new_combined'
                                    )
                                dict_index_mapping_from_component_to_combined[
                                    int_entry
                                ] = dict_str_entry_to_int_entry[
                                    str_entry
                                ]  # retrieve int_entry of combined axis --> int_entry of individual axis mapping
                            # update 'int_pos_component'
                            int_pos_component += self.int_max_num_entries_per_batch
                        l_dict_index_mapping_interleaved.append(
                            dict(
                                (
                                    dict_index_mapping_from_component_to_combined[
                                        int_entry_component
                                    ],
                                    int_entry_component,
                                )
                                for int_entry_component in dict_index_mapping_from_component_to_combined
                            )
                        )  # update 'l_dict_index_mapping_interleaved'
                        l_dict_index_mapping_from_component_to_combined.append(
                            dict_index_mapping_from_component_to_combined
                        )  # retrieve mapping from component to combined axis coordinates

                        int_num_records = len(
                            dict_index_mapping_from_component_to_combined
                        )  # retrieve the number of mapping records for the current axis object
                        l_int_num_records.append(
                            int_num_records
                        )  # collect the number of records for the current axis object
                        # convert 'dict_index_mapping_from_component_to_combined' to a numpy array
                        arr = np.zeros((int_num_records, 2), dtype=np.float64)
                        for i, int_entry_component in enumerate(
                            dict_index_mapping_from_component_to_combined
                        ):
                            arr[i, 0] = dict_index_mapping_from_component_to_combined[
                                int_entry_component
                            ]  # set combined axis
                            arr[i, 1] = int_entry_component  # set component axis
                        # write converted array containing the mapping to the zarr object
                        za[int_pos_mapping : int_pos_mapping + int_num_records] = arr
                        # update 'int_pos_mapping'
                        int_pos_mapping += int_num_records

                    # write collected metadata to the zarr object
                    dict_metadata = {"l_int_num_records": l_int_num_records}
                    za.attrs["dict_metadata"] = dict_metadata

                    """ write the combined axis """
                    if flag_load_all_string_representations_from_components:
                        """prepare data for the axis object write barcodes and features files to zarr objects"""
                        # initialize
                        int_num_entries = len(
                            dict_str_entry_to_int_entry
                        )  # retrieve the number of entries
                        index_chunk = 0  # initialize chunk size
                        int_pos = 0  # initialize the start position

                        # write zarr object for random access of string representation of the entries of the axis object

                        num_available_columns_string_representation = self._l_ax[
                            0
                        ].num_available_columns_string_representation  # use the number of string representation columns from the first axis object as the number of available string representation columns of the combined axis
                        za = zarr.open(
                            f"{path_folder}{name_axis}.str.zarr",
                            mode="w",
                            shape=(
                                int_num_entries,
                                num_available_columns_string_representation,
                            ),
                            chunks=(int_num_entries_in_a_chunk, 1),
                            dtype=str,
                            synchronizer=zarr.ThreadSynchronizer(),
                        )  # string object # individual columns will be chucked, so that each column can be retrieved separately.

                        # create a folder to save a chunked string representations
                        path_folder_str_chunks = f"{path_folder}{name_axis}.str.chunks/"
                        filesystem_operations(
                            "mkdir", path_folder_str_chunks, exist_ok=True
                        )
                        za_str_chunks = zarr.group(path_folder_str_chunks)
                        za_str_chunks.attrs["dict_metadata"] = {
                            "int_num_entries": int_num_entries,
                            "int_num_of_entries_in_a_chunk": int_num_entries_in_a_chunk,
                        }  # write essential metadata for str.chunks

                        while (
                            int_pos < int_num_entries
                        ):  # until all entries were processed.
                            int_num_entries_chunk = min(
                                int_num_entries_in_a_chunk, int_num_entries - int_pos
                            )  # retrieve the number of entries in a chunk

                            arr_str_chunk = np.zeros(
                                (
                                    int_num_entries_chunk,
                                    num_available_columns_string_representation,
                                ),
                                dtype=object,
                            )  # initialize an array containing a chunk of string representations

                            ba_flag_retrieved_chunk = bitarray(
                                int_num_entries_chunk
                            )  # initialize the bitarray of flags indicating which entry has been retrieved.
                            ba_flag_retrieved_chunk.setall(0)  # all entries to False

                            for ax, dict_index_mapping_interleaved in zip(
                                self._l_ax, l_dict_index_mapping_interleaved
                            ):  # for each component axis object, retrieve axis object and its mapping dictionary
                                l_int_entry_combined, l_int_entry_component = (
                                    [],
                                    [],
                                )  # initialize list of 'int_entry_combined' and 'int_entry_component' for the current chunk
                                for int_entry_combined in range(
                                    int_pos,
                                    min(
                                        int_num_entries,
                                        int_pos + int_num_entries_in_a_chunk,
                                    ),
                                ):
                                    if (
                                        int_entry_combined
                                        in dict_index_mapping_interleaved
                                        and not ba_flag_retrieved_chunk[
                                            int_entry_combined - int_pos
                                        ]
                                    ):  # if the 'int_entry_combined' exist in the current axis and the data has not been retrieved.
                                        # collect 'int_entry_component' for the current batch
                                        l_int_entry_combined.append(int_entry_combined)
                                        l_int_entry_component.append(
                                            dict_index_mapping_interleaved[
                                                int_entry_combined
                                            ]
                                        )
                                        # update bitarray mask
                                        ba_flag_retrieved_chunk[
                                            int_entry_combined - int_pos
                                        ] = 1  # indicate that the data for the current entry has been retrieved.
                                if (
                                    len(l_int_entry_combined) > 0
                                ):  # if the current chunk for the current axis object contains valid entries
                                    arr_str_chunk[
                                        np.array(l_int_entry_combined, dtype=int)
                                        - int_pos
                                    ] = ax.get_str(
                                        l_int_entry_component,
                                        np.arange(
                                            num_available_columns_string_representation
                                        ),
                                    )  # correct the coordinates # retrieve string representations and save to the combined array

                            sl_chunk = slice(
                                int_pos,
                                min(
                                    int_num_entries,
                                    int_pos + int_num_entries_in_a_chunk,
                                ),
                            )
                            za[sl_chunk] = arr_str_chunk  # set str.zarr
                            # set str.chunks
                            for index_col, arr_val in enumerate(arr_str_chunk.T):
                                with open(
                                    f"{path_folder_str_chunks}{index_chunk}.{index_col}",
                                    "wt",
                                ) as newfile:  # similar organization to zarr
                                    newfile.write(
                                        base64_encode(
                                            gzip_bytes(
                                                ("\n".join(arr_val) + "\n").encode()
                                            )
                                        )
                                    )
                            int_pos += int_num_entries_in_a_chunk  # update 'int_pos'
                            index_chunk += 1  # update 'index_chunk'
                # set attributes
                self._l_dict_index_mapping_interleaved = l_dict_index_mapping_interleaved  # save a list of constructed dictionaries for indices mapping as an attribute
                self._l_dict_index_mapping_from_component_to_combined = l_dict_index_mapping_from_component_to_combined  # save a list of dictionaries mapping component coordinates to those of the combined axis.
                self._l_dict_index_mapping_from_combined_to_component = (
                    self._l_dict_index_mapping_interleaved
                )
            else:
                # %% COMBINED-STACKED %%
                l_cumulated_len_stacked = (
                    []
                )  # a list of cumulated number of entries of stacked axis objects
                l_dict_index_mapping_from_component_to_combined = (
                    []
                )  # retrieve component -> combined axis mapping
                l_dict_index_mapping_from_combined_to_component = (
                    []
                )  # retrieve combined -> component axis mapping
                int_pos = 0  # initialize the start position
                for ax in self._l_ax:
                    l_dict_index_mapping_from_component_to_combined.append(
                        IndexMappingDictionary(
                            int_length_component_axis=ax.int_num_entries,
                            int_offset=int_pos,
                            flag_component_to_combined=True,
                        )
                    )
                    l_dict_index_mapping_from_combined_to_component.append(
                        IndexMappingDictionary(
                            int_length_component_axis=ax.int_num_entries,
                            int_offset=int_pos,
                            flag_component_to_combined=False,
                        )
                    )
                    l_cumulated_len_stacked.append(int_pos)  # update stacked length
                    int_pos += ax.int_num_entries  # update 'int_pos'
                l_cumulated_len_stacked.append(int_pos)  # update stacked length
                # set attributes
                self._l_dict_index_mapping_from_component_to_combined = (
                    l_dict_index_mapping_from_component_to_combined
                )
                self._l_dict_index_mapping_from_combined_to_component = (
                    l_dict_index_mapping_from_combined_to_component
                )
                self._l_cumulated_len_stacked = l_cumulated_len_stacked

                # compose/load string representations
                path_folder_str_rep = f"{path_folder}{name_axis}.str.zarr"  # define a folder where string representations will be saved
                if not zarr_exists(
                    path_folder_str_rep
                ):  # if the output zarr object does not exists
                    """write the combined axis"""
                    """ prepare data for the axis object write barcodes and features files to zarr objects """
                    # initialize
                    int_num_entries = sum(
                        ax.int_num_entries for ax in self._l_ax
                    )  # retrieve the total number of entries in the combined-stacked axis
                    index_chunk = 0  # initialize chunk size
                    int_pos = 0  # initialize the start position
                    num_available_columns_string_representation = self._l_ax[
                        0
                    ].num_available_columns_string_representation  # use the number of string representation columns from the first axis object as the number of available string representation columns of the combined axis
                    arr_str_rep_buffer = np.zeros(
                        (
                            int_num_entries_in_a_chunk * 2,
                            num_available_columns_string_representation,
                        ),
                        dtype=object,
                    )  # set buffer size as 2 * 'int_num_entries_in_a_chunk'
                    len_arr_str_rep_buffer = 0  # track the number of entries in the buffer 'arr_str_rep_buffer'

                    # write a zarr object for the random access of string representation of the entries of the axis object
                    if flag_load_all_string_representations_from_components:
                        za = zarr.open(
                            f"{path_folder}{name_axis}.str.zarr",
                            mode="w",
                            shape=(
                                int_num_entries,
                                num_available_columns_string_representation,
                            ),
                            chunks=(int_num_entries_in_a_chunk, 1),
                            dtype=str,
                            synchronizer=zarr.ThreadSynchronizer(),
                        )  # string object # individual columns will be chucked, so that each column can be retrieved separately.

                        # create a folder to save a chunked string representations (for web application)
                        path_folder_str_chunks = f"{path_folder}{name_axis}.str.chunks/"
                        filesystem_operations(
                            "mkdir", path_folder_str_chunks, exist_ok=True
                        )
                        za_str_chunks = zarr.group(path_folder_str_chunks)
                        za_str_chunks.attrs["dict_metadata"] = {
                            "int_num_entries": int_num_entries,
                            "int_num_of_entries_in_a_chunk": int_num_entries_in_a_chunk,
                        }  # write essential metadata for str.chunks

                        for ax in self._l_ax:  # iterate over each axis object
                            int_pos_component = 0  # initialize 'int_pos_component' for the iteration of the current axis object
                            while (
                                int_pos_component < ax.int_num_entries
                            ):  # until all entries of the current component were processed.
                                int_num_entries_batch = min(
                                    int_num_entries_in_a_chunk,
                                    ax.int_num_entries - int_pos_component,
                                )  # retrieve the number of entries in a batch (a chunk)
                                # write zarr object
                                arr_str_rep_batch = ax.get_str(
                                    slice(
                                        int_pos_component,
                                        int_pos_component + int_num_entries_batch,
                                    ),
                                    np.arange(
                                        num_available_columns_string_representation
                                    ),
                                )  # retrieve string representations for the current batch
                                za[
                                    int_pos
                                    + int_pos_component : int_pos
                                    + int_pos_component
                                    + int_num_entries_batch
                                ] = arr_str_rep_batch

                                # update the string representation buffer for 'str.chunks'
                                arr_str_rep_buffer[
                                    len_arr_str_rep_buffer : len_arr_str_rep_buffer
                                    + int_num_entries_batch
                                ] = arr_str_rep_batch
                                del arr_str_rep_batch
                                len_arr_str_rep_buffer += (
                                    int_num_entries_batch  # update length of the buffer
                                )
                                # write 'str.chunks'
                                if (
                                    len_arr_str_rep_buffer >= int_num_entries_in_a_chunk
                                ):  # if more than a chunk of data is present in the buffer, write a chunk
                                    for index_col, arr_val in enumerate(
                                        arr_str_rep_buffer[
                                            :int_num_entries_in_a_chunk
                                        ].T
                                    ):
                                        with open(
                                            f"{path_folder_str_chunks}{index_chunk}.{index_col}",
                                            "wt",
                                        ) as newfile:  # similar organization to zarr
                                            newfile.write(
                                                base64_encode(
                                                    gzip_bytes(
                                                        (
                                                            "\n".join(arr_val) + "\n"
                                                        ).encode()
                                                    )
                                                )
                                            )
                                    arr_str_rep_buffer[
                                        :int_num_entries_in_a_chunk
                                    ] = arr_str_rep_buffer[
                                        int_num_entries_in_a_chunk:
                                    ]  # remove the values written to the disk as a chunk from the buffer
                                    len_arr_str_rep_buffer -= int_num_entries_in_a_chunk  # update length of the buffer
                                    index_chunk += 1  # update 'index_chunk'

                                int_pos_component += (
                                    int_num_entries_batch  # update 'int_pos_component'
                                )
                            int_pos += ax.int_num_entries  # update 'int_pos'

                        if (
                            len_arr_str_rep_buffer >= 0
                        ):  # if buffer is not empty, write the remaining data as a chunk
                            for index_col, arr_val in enumerate(
                                arr_str_rep_buffer[:len_arr_str_rep_buffer].T
                            ):
                                with open(
                                    f"{path_folder_str_chunks}{index_chunk}.{index_col}",
                                    "wt",
                                ) as newfile:  # similar organization to zarr
                                    newfile.write(
                                        base64_encode(
                                            gzip_bytes(
                                                ("\n".join(arr_val) + "\n").encode()
                                            )
                                        )
                                    )
                        del arr_str_rep_buffer

        # initialize the mapping dictionaries
        self._dict_str_to_i = None
        self._dict_i_to_str = None

        self.meta = ZarrDataFrame(
            f"{path_folder}{name_axis}.num_and_cat.zdf",
            l_zdf=list(ax.meta for ax in self._l_ax)
            if self._l_ax is not None
            else None,
            index_zdf_data_source_when_interleaved=self.index_ax_data_source_when_interleaved,
            l_dict_index_mapping_interleaved=self._l_dict_index_mapping_interleaved,
            l_dict_index_mapping_from_combined_to_component=self._l_dict_index_mapping_from_combined_to_component,
            l_dict_index_mapping_from_component_to_combined=self._l_dict_index_mapping_from_component_to_combined,
            ba_filter=ba_filter,
            mode=mode,
            path_folder_mask=None
            if path_folder_mask is None
            else f"{path_folder_mask}{name_axis}.num_and_cat.zdf",
            flag_is_read_only=self._flag_is_read_only,
            zarrspinlockserver=self._zsls,
            int_num_cpus=int_num_cpus,
            flag_spawn=self.flag_spawn,
            **dict_kw_zdf,
        )  # open a ZarrDataFrame with a given filter
        self.int_num_entries = (
            self.meta._n_rows_unfiltered
        )  # retrieve number of entries

        self.filter = ba_filter  # set filter

        # initialize viewer (coordinate converter, a dictionary for converting coordinates)
        # set viewer settings
        self._dict_kw_view = dict_kw_view
        self.dict_change = None  # initialize view
        self._dict_change_backup = None

    @property
    def path_folder(self):
        """# 2023-04-12 17:19:28"""
        return self._path_folder

    @property
    def flag_spawn(self):
        """# 2023-03-26 01:35:37
        return 'flag_spawn' attribute
        """
        return self._flag_spawn

    @property
    def is_remote(self):
        """# 2022-09-03 17:17:32
        return True if the RamData is located remotely
        """
        return is_remote_url(self._path_folder)

    @property
    def m(self):
        """# 2023-02-14 23:27:20
        shorthand
        """
        return self.meta

    @property
    def int_num_cpus(self):
        """# 2023-01-20 17:41:25
        number of cpu cores to use for RamDataAxis operations
        """
        return self._int_num_cpus

    @int_num_cpus.setter
    def int_num_cpus(self, val):
        """# 2023-01-20 17:41:25
        change the number of cpu cores to use for RamDataAxis operations
        """
        self._int_num_cpus = val
        self.meta.int_num_cpus = val

    @property
    def locking_server(self):
        """# 2022-12-23 00:02:37
        return 'ZarrSpinLockServer' object
        """
        return self._zsls

    @locking_server.setter
    def locking_server(self, locking_server_new):
        """# 2022-12-23 00:02:43"""
        self._zsls = (
            locking_server_new  # set 'ZarrSpinLockServer' of the current object
        )
        self.meta._zsls = (
            locking_server_new  # set 'ZarrSpinLockServer' of the metadata ZDF
        )

    @property
    def n_components(self):
        """# 2022-09-08 18:07:55
        return the number of components when current RamDataAxis is in 'combined' mode. if the current object is not in a 'combined' mode,
        """
        int_n_components = 0  # set default
        if self.is_combined:
            int_n_components = len(self._l_ax)  # retrieve the number of components
        return int_n_components

    @property
    def index_ax_data_source_when_interleaved(self):
        """# 2022-08-28 15:11:47
        return the index of the axis to retrieve metadata when interleaved
        """
        return self._index_ax_data_source_when_interleaved

    @index_ax_data_source_when_interleaved.setter
    def index_ax_data_source_when_interleaved(
        self, index_ax_data_source_when_interleaved
    ):
        """# 2022-08-28 15:11:47
        set the index of the axis to retrieve metadata when interleaved
        """
        assert (
            0 <= index_ax_data_source_when_interleaved < len(self._l_ax)
        )  # check whether the 'index_ax_data_source_when_interleaved' is in a valid range
        self._index_ax_data_source_when_interleaved = index_ax_data_source_when_interleaved  # update 'index_ax_data_source_when_interleaved'
        self.meta.index_zdf_data_source_when_interleaved = (
            self._index_ax_data_source_when_interleaved
        )  # update 'index_zdf_data_source_when_interleaved' of the metadata

    @property
    def is_combined(self):
        """# 2022-08-27 11:35:09
        return True if current axis is in 'combined' mode
        """
        return self._l_ax is not None

    @property
    def is_interleaved(self):
        """# 2022-08-27 11:35:13
        return True if current axis is 'interleaved', 'combined' axis
        """
        return self._l_dict_index_mapping_interleaved is not None

    @property
    def are_all_entries_active(self):
        """# 2022-12-15 08:48:56
        return True if all entries of the current axis object are active
        """
        return len(self.meta) == self.int_num_entries

    def _convert_to_bitarray(self, ba_filter):
        """# 2022-08-03 02:21:21
        handle non-None filter objects and convert these formats to the bitarray filter object
        """
        """ handle non-bitarray input types """
        if self.int_num_entries != len(
            ba_filter
        ):  # when the length of the input array does not equal to the number of entries in the current axis, input is a list of integer indices of the active entries
            # directly convert the list of integer indices to the bitarray
            ba = bitarray(self.int_num_entries)
            ba.setall(0)
            for int_entry in ba_filter:
                ba[int_entry] = True
            return ba

        # handle when a list type has been given (convert it to np.ndarray)
        if isinstance(ba_filter, list) or (
            isinstance(ba_filter, np.ndarray) and ba_filter.dtype != bool
        ):  # change to target dtype
            ba_filter = np.array(ba_filter, dtype=bool)
        # handle when a numpy ndarray has been given (convert it to bitarray)
        if isinstance(ba_filter, np.ndarray):
            ba_filter = BA.to_bitarray(ba_filter)
        assert isinstance(ba_filter, bitarray)  # check the return is bitarray object
        return ba_filter

    def __iter__(self):
        """# 2022-07-02 22:16:56
        iterate through valid entries in the axis, according to the filter and whether the string representations are loaded or not. if string representations were loaded, iterate over string representations.
        """
        return (
            (
                BA.to_integer_indices(self.filter)
                if self.filter is not None
                else np.arange(len(self))
            )
            if self._dict_str_to_i is None
            else self._dict_str_to_i
        ).__iter__()

    def __len__(self):
        """# 2022-08-21 15:31:48
        returns the number of entries in the Axis. when view is active, the length after applying the view will be returned. when view is absent, the number of all entries will be returned, regardless of whether a filter is active or not.
        """
        return (
            (
                self._l_ax[self._int_index_component_destination].meta.n_rows
                if self.is_destination_component_set
                else self.meta.n_rows
            )
            if self.is_view_active
            else self.int_num_entries
        )

    def reset(self):
        """# 2023-03-11 01:15:00
        reset the filter
        """
        self.filter = None

    @property
    def is_view_active(self):
        """# 2022-08-21 15:31:44
        return true if a view is active
        """
        return self.dict_change is not None

    def set_view(self, dict_change):
        """# 2023-02-21 16:01:10
        set a view using the given 'dict_change'
        """
        self.dict_change = dict_change  # load 'dict_change'

    def create_view(
        self,
        index_component: Union[None, int] = None,
        flag_return_valid_entries_in_the_currently_active_layer: bool = False,
        l_entry_view: Union[None, list] = None,
        int_index_str_rep: int = 0,
    ):
        """# 2023-02-22 20:53:08
        build 'dict_change' (dictionaries for conversion of coordinates) from the given filter or the given list of integer or string representations, creating a view of the current 'Axis'
        automatically set filter using the mask containing all active entries with valid data if filter is not active

        for example, when filter is
         0123456789  - index
        '1000101110' - filter

        then, dict_change will be { 0 : 0, 4 : 1, 6 : 2, 7 : 3, 8 : 4 }
        when the number of active entries in an exis > 10% (or above any proportion that can set by 'float_min_proportion_of_active_entries_in_an_axis_for_using_array'), an array with the same length will be used for the conversion of coordinates

        'float_min_proportion_of_active_entries_in_an_axis_for_using_array' : a threshold for the transition from dictionary to array for the conversion of coordinates. empirically, dictionary of the same length takes about ~10 times more memory than the array
        'dtype' : dtype of array that will be used as 'dictionary'
        index_component : Union[ None, int ] = None : the index of a component RamData to retrieve view.
        flag_return_valid_entries_in_the_currently_active_layer : bool = True # if filter does not exist, use apply a filter containing all the valid entries of the currently active layer.
        l_entry_view : Union[ None, list ] = None, # list of string or integer representations of the entries from which to create a view. (it should contain unique values only and no duplicated values)
        int_index_str_rep : int = 0, # 'int_index_str_rep' for creating a view from 'l_entry'
        """
        # create view of a component RamData
        if (
            self.is_combined and index_component is not None
        ):  # if current Axis is in the 'combined' mode and 'index_component' has been given
            ax = self._l_ax[index_component]  # retrieve the axis of the component
            ax.create_view(
                index_component=None,
                l_entry_view=l_entry_view,
                int_index_str_rep=int_index_str_rep,
            )  # create view of the component
            dict_change = ax.dict_change  # retrieve the mapping
            ax.destroy_view()
            # set view
            self.dict_change = dict_change
            return

        # retrieve settings to create a view
        float_min_proportion_of_active_entries_in_an_axis_for_using_array = (
            0.1
            if "float_min_proportion_of_active_entries_in_an_axis_for_using_array"
            not in self._dict_kw_view
            else self._dict_kw_view[
                "float_min_proportion_of_active_entries_in_an_axis_for_using_array"
            ]
        )
        dtype = (
            np.int32
            if "dtype" not in self._dict_kw_view
            else self._dict_kw_view["dtype"]
        )

        # retrieve a flag
        flag_using_filter_to_create_a_view = l_entry_view is None
        dict_change = None  # initialize 'dict_change'

        if flag_using_filter_to_create_a_view:
            """
            using a filter to create a view
            """
            # automatically set filter using the mask containing all active entries with valid data if filter is not active
            if self.filter is None:
                self.filter = self.all(
                    flag_return_valid_entries_in_the_currently_active_layer=flag_return_valid_entries_in_the_currently_active_layer
                )

            ba = self.filter
            if (
                ba is not None and ba.count() < self.int_num_entries
            ):  # only build 'dict_change' if a filter is active or at least one entry is not active
                n = len(ba)
                n_active_entries = ba.count()
                # initialize dictionary
                dict_change = (
                    np.full(n, -1, dtype=dtype)
                    if (n_active_entries / n)
                    > float_min_proportion_of_active_entries_in_an_axis_for_using_array
                    else dict()
                )  # implement a dictionary using an array if the proportion of active entries in the axis is larger than the given threshold to reduce the memory footprint and increase the efficiency of conversion process # when an array is used for 'dict_change', -1 indicates an invalid mapping
                for i, e in enumerate(
                    BA.to_integer_indices(ba)
                ):  # iterate through 'int_entry' of the active entries
                    dict_change[e] = i
        elif len(l_entry_view) > 0:  # if 'l_entry' is valid
            """
            using a list of integer/string representations of the entries to create a view
            """
            l_int_entry_view = l_entry_view  # assumes 'l_entry_view' contains 'l_int_entry_view' integer values by default
            if isinstance(
                l_entry_view[0], str
            ):  # if string representations of the entries were given
                # load mapping for string representations of the current axis using the given 'int_index_str_rep'
                self.load_str(int_index_col=int_index_str_rep)
                dict_mapping = self.map_str  # retrieve the mapping of the current axis
                l_int_entry_view = list(
                    dict_mapping[str_entry_view]
                    if str_entry_view in dict_mapping
                    else -1
                    for str_entry_view in l_entry_view
                )  # convert to 'l_int_entry_view'

            # initialize dictionary
            n_active_entries = len(
                l_int_entry_view
            )  # assumes all given entries for creating a view is valid
            n = self.int_num_entries
            dict_change = (
                np.full(n, -1, dtype=dtype)
                if (n_active_entries / n)
                > float_min_proportion_of_active_entries_in_an_axis_for_using_array
                else dict()
            )  # implement a dictionary using an array if the proportion of active entries in the axis is larger than the given threshold to reduce the memory footprint and increase the efficiency of conversion process # when an array is used for 'dict_change', -1 indicates an invalid mapping
            for int_index_view, int_entry_view in enumerate(l_int_entry_view):
                if (
                    0 <= int_entry_view < self.int_num_entries
                ):  # if 'int_entry_view' is in a valid range
                    dict_change[int_entry_view] = int_index_view  # build 'dict_change'
        self.dict_change = dict_change  # load 'dict_change'

    def destroy_view(self):
        """# 2022-07-16 15:23:01
        unload 'self.dict_change' (dictionaries for conversion of coordinates), destroying the current view
        """
        self.dict_change = None

    def backup_view(self):
        """# 2022-08-20 17:25:12
        backup view
        """
        self._dict_change_backup = self.dict_change  # back up view
        self.destroy_view()  # destroy view

    def restore_view(self):
        """# 2022-08-20 17:25:12
        restore view
        """
        self.dict_change = self._dict_change_backup
        self._dict_change_backup = None

    @property
    def filter(self):
        """# 2022-06-24 22:20:43
        return a bitarray filter
        """
        return self._ba_filter

    @filter.setter
    def filter(self, ba_filter):
        """# 2022-09-12 17:50:01
        set a new bitarray filter on the Axis and the RamData object to which the current axis belongs to.

        a given mask will be further masked so that only entries with a valid count data is included in the resulting filter

        """
        """ convert other formats to bitarray if a filter has been given """
        self.destroy_view()  # if a filter has been updated, 'dict_change' will be unloaded

        if ba_filter is not None:
            ba_filter = self._convert_to_bitarray(
                ba_filter
            )  # convert mask to bitarray filter

        # propagate the filter
        self.meta.filter = ba_filter  # change filter of metadata zdf
        self._ba_filter = ba_filter  # set the filter of current axis object
        # set the filter of layer object of the RamData to which the current axis object has been attached.
        if (
            self._ramdata is not None and self._ramdata.layer is not None
        ):  # if a layor object has been loaded in the RamData to which the current Axis object belongs to.
            setattr(self._ramdata._layer, f"ba_filter_{self._name_axis}", ba_filter)

        # propagate the filter to component RamData objects
        if self.is_combined:
            # %% COMBINED %%
            if ba_filter is None:  # if filter is removed
                # remove filter from all axis objects
                for ax in self._l_ax:
                    ax.filter = None
            else:  # if filter is being set
                if self.is_interleaved:
                    # %% COMBINED - INTERLEAVED %%
                    for ax, dict_index_mapping_interleaved in zip(
                        self._l_ax, self._l_dict_index_mapping_interleaved
                    ):
                        # initialize filter for the current axis object
                        ba_comp = bitarray(ax.meta._n_rows_unfiltered)
                        ba_comp.setall(0)
                        # compose filter
                        for int_entry_combined in BA.find(
                            ba_filter
                        ):  # iterate active entries in the combined axis
                            if (
                                int_entry_combined in dict_index_mapping_interleaved
                            ):  # if the active entry also exists in the current axis, update the filter
                                ba_comp[
                                    dict_index_mapping_interleaved[int_entry_combined]
                                ] = 1

                        ax.filter = ba_comp  # set filter of the component axis
                else:
                    # %% COMBINED - STACKED %%
                    # for stacked axis, split the given filter into smaller filters for each zdf
                    int_pos = 0
                    for ax in self._l_ax:
                        ax.filter = ba_filter[
                            int_pos : int_pos + ax.meta._n_rows_unfiltered
                        ]  # apply a subset of filter
                        int_pos += ax.meta._n_rows_unfiltered  # update 'int_pos'

    def get_filter_combined_from_filter_component(
        self, ba_filter: bitarray, int_index_component: int
    ):
        """# 2022-09-23 17:16:19

        ba_filter : bitarray # bitarray object of the component axis
        int_index_component : int #

        """
        if self.is_combined:  # only return if 'combined' mode is active
            # retrieve target axis
            ax = self._l_ax[int_index_component]
            dict_index_mapping_from_component_to_combined = (
                self._l_dict_index_mapping_from_component_to_combined[
                    int_index_component
                ]
            )
            # make sure that the number of entries in the given filter is the same with the length of the component axis
            if len(ba_filter) != ax.int_num_entries:
                return

            # initialize the output bitarray
            ba_filter_combined = bitarray(self.int_num_entries)
            ba_filter_combined.setall(0)

            # transfer component entries to combined entries
            for int_entry_component in BA.find(ba_filter):
                ba_filter_combined[
                    dict_index_mapping_from_component_to_combined[int_entry_component]
                ] = True

            # return the filter of the combined axis
            return ba_filter_combined

    @property
    def columns(self):
        """# 2022-10-29 23:20:43
        a shortcut for self.meta.columns
        """
        return self.meta.columns

    @property
    def ba_active_entries(self):
        """# 2022-07-16 17:38:04

        return a bitarray object containing currently active entries in the Axis.
        if a filter is active, return the current filter
        if a filter is not active, return the return value of Axis.all( flag_return_valid_entries_in_the_currently_active_layer = True )
        """
        return (
            self.all(flag_return_valid_entries_in_the_currently_active_layer=True)
            if self.filter is None
            else self.filter
        )

    def get_str(self, queries=None, int_index_col: Union[int, None] = None):
        """# 2022-09-22 12:07:01
        get string representations of the queries

        'queries' : queries (slice, integer indices, bitarray, etc.) of the entries for which string representations will be loaded. if None is given, all entries will be retrieved.
        int_index_col : Union[ int, None ] = None : the index of the column containing string representation to retrieve. if a single integer index is given, retrieve values from a single column. If a list or a tuple of integer indices are given, values of the columns will be retrieved.
        """
        # retrieve all entries for the 'default' queries
        if queries is None:
            queries = slice(None, None)
        # set default value for 'int_index_col'
        if int_index_col is None:
            int_index_col = self.int_index_str_rep
        # check whether string representation of the entries of the given axis is available
        path_folder_str_zarr = f"{self._path_folder if self._path_folder_mask is None else self._path_folder_mask}{self._name_axis}.str.zarr"  # retrieve sink column path

        # perform lazy-loading
        self.meta.lazy_load(
            queries,
            name_col_sink=None,
            flag_mode_write=False,  # read-mode, without modification of original string representations
            path_column_sink=path_folder_str_zarr,
            path_column_source=f"{self._path_folder}{self._name_axis}.str.zarr",  # retrieve column path
            l_path_column_source=list(
                f"{ax._path_folder}{ax._name_axis}.str.zarr"
                if zarr_exists(f"{ax._path_folder}{ax._name_axis}.str.zarr")
                else None
                for ax in self._l_ax
            )
            if self.is_combined
            else None,
            name_col_availability="__str__availability__",
            flag_retrieve_from_all_interleaved_components=True,  # retrieve string representations from all component
        )

        # open a zarr object containing the string representation of the entries
        if zarr_exists(path_folder_str_zarr):
            za = zarr.open(path_folder_str_zarr, "r")

            # handle bitarray query
            if isinstance(queries, bitarray):
                if (
                    queries.count() > len(queries) / 8
                ):  # if the number of active entries is larger than the threshold, use the boolean array form
                    queries = BA.to_array(queries)
                else:  # if the number of active entries is smaller than the threshold, use the
                    queries = BA.to_integer_indices(queries)

            return za.get_orthogonal_selection((queries, int_index_col))

    def iterate_str(
        self,
        int_num_entries_in_a_batch: int = 1000,
        int_index_col: Union[int, None] = None,
    ):
        """# iterate through string representations of the active entries of the current axis object

        int_num_entries_in_a_batch : int = 1000 # the number of entries that will be included in a batch
        int_index_col : Union[ int, None ] = None : the index of the column containing string representation to retrieve. if a single integer index is given, retrieve values from a single column. If a list or a tuple of integer indices are given, values of the columns will be retrieved.
        """
        l_int_entry_in_a_batch = []  # initialize a batch container
        for int_entry in (
            range(self.int_num_entries) if self.filter is None else BA.find(self.filter)
        ):  # iterate through integer indices of the active entries
            l_int_entry_in_a_batch.append(int_entry)
            # if a batch is full, flush the batch
            if len(l_int_entry_in_a_batch) >= int_num_entries_in_a_batch:
                yield {
                    "l_int_entry": l_int_entry_in_a_batch,
                    "l_str_entry": self.get_str(
                        queries=l_int_entry_in_a_batch, int_index_col=int_index_col
                    ),
                }
                l_int_entry_in_a_batch = []  # initialize the next batch
        # if there are remaining entries, flush the batch
        if len(l_int_entry_in_a_batch) > 0:
            yield {
                "l_int_entry": l_int_entry_in_a_batch,
                "l_str_entry": self.get_str(
                    queries=l_int_entry_in_a_batch, int_index_col=int_index_col
                ),
            }

    def load_str(
        self,
        int_index_col=None,
        float_min_proportion_of_active_entries_for_using_array_as_dict: float = 0.1,
        flag_load_list_of_str_repr_for_autocompletion: bool = True,
        flag_load_without_updating_mapping: bool = False,
    ):
        """# 2022-09-12 02:28:49
        load string representation of all the active entries of the current axis, and retrieve a mapping from string representation to integer representation

        'int_index_col' : default value is 'self.int_index_str_rep'
        float_min_proportion_of_active_entries_for_using_array_as_dict : float = 0.1 : A threshold for the transition from dictionary to array datatype for the mapping. empirically, dictionary of the same length takes about ~10 times more memory than the array.
            By default, when the number of active entries in an axis > 10% (or above any proportion that can set by 'float_min_proportion_of_active_entries_for_using_array_as_dict'), an array representing all rows will be used for the mapping
        flag_load_list_of_str_repr_for_autocompletion : bool = True # load the list of string representations (which is required for autocompletion features)
        flag_load_without_updating_mapping : bool = False, # If True, 'flag_load_without_updating_mapping' load string representations without updating mapping of string entries. If True, 'str_repr_for_autocompletion' will not be loaded, too.
        """
        # set default value for 'int_index_col'
        if int_index_col is None:
            int_index_col = self.int_index_str_rep
        # check whether string representation of the entries of the given axis is available
        path_folder_str_zarr = f"{self._path_folder}{self._name_axis}.str.zarr"

        # compose a pair of dictionaries for the conversion
        arr_int_entry = (
            np.arange(self.int_num_entries)
            if self.filter is None
            else BA.to_integer_indices(self.filter)
        )  # retrieve integer representations of the entries
        arr_str = self.get_str(
            queries=arr_int_entry, int_index_col=int_index_col
        )  # retrieve string representations of the entries

        """
        Update mapping
        """
        if not flag_load_without_updating_mapping:
            # str > integer mapping
            self._dict_str_to_i = dict((e, i) for e, i in zip(arr_str, arr_int_entry))

            # integer > str mapping
            n = (
                self.meta._n_rows_unfiltered
            )  # retrieve the number of entries in the unfiltered metadata
            dict_i_to_str = (
                np.zeros(n, dtype=object)
                if (self.meta.n_rows / n)
                > float_min_proportion_of_active_entries_for_using_array_as_dict
                else dict()
            )  # implement a dictionary using an array if the proportion of active rows of ZarrDataFrame is larger than the given threshold to reduce the memory footprint and increase the efficiency of access
            for int_entry, str_entry in zip(
                arr_int_entry, arr_str
            ):  # iterate through data values of the active rows
                dict_i_to_str[int_entry] = str_entry
            self._dict_i_to_str = dict_i_to_str
            del dict_i_to_str

            # load of list of string representations
            self._l_str = None
            if flag_load_list_of_str_repr_for_autocompletion:
                self._l_str = list(
                    arr_str
                )  # load the list of string representations (for autocompletion in IPython environment)

        if self.verbose:
            logger.info(
                f"[Axis {self._name_axis}] completed loading of {len( arr_str )} number of strings"
            )
        return arr_str  # return loaded strings

    @property
    def l_str(self):
        """# 2023-01-21 15:35:14
        list of string representations that are currently loaded in the axis.
        """
        return self._l_str

    def unload_str(self):
        """# 2022-06-25 09:36:59
        unload a mapping between string representations and integer representations.
        """
        self._dict_str_to_i = None
        self._dict_i_to_str = None

    def _ipython_key_completions_(self):
        """# 2023-01-21 14:50:07
        (ipython integration) method for supporting autocompletion of feature names that are already loaded in memory
        """
        if (
            self.l_str is not None
        ):  # check whether a list of str representations were loaded
            return self.l_str

    @property
    def num_available_columns_string_representation(self):
        """# 2022-08-28 11:49:04
        return the number of columns containing string representations
        """
        if not hasattr(
            self, "_num_available_columns_string_representation"
        ):  # if the attribute has not been calculated
            # retrieve the number of available columns containing string representations
            self._num_available_columns_string_representation = zarr.open(
                f"{self._path_folder}{self._name_axis}.str.zarr", "r"
            ).shape[1]
        return self._num_available_columns_string_representation

    @property
    def flag_str_repr_loaded(self):
        """# 2022-10-29 20:31:56
        return a flag indicating whether the string representations were loaded
        """
        return self.map_str is not None

    @property
    def map_str(self):
        """# 2022-06-25 09:31:32
        return a dictionary for mapping string representation to integer representation
        """
        return self._dict_str_to_i

    @property
    def map_int(self):
        """# 2022-06-25 09:31:32
        return a dictionary for mapping integer representation to string representation
        """
        return self._dict_i_to_str

    def __getitem__(self, l):
        """# 2022-07-14 00:42:20
        a main functionality of 'Axis' class
        translate a given list of entries / slice / mask (bitarray/boolean_array), and return a bitarray mask containing valid entries

        inputs:
        [list of entries / slice / mask (bitarray/boolean_array)]

        returns:
        [a list of valid integer representation]
        """
        """ initialize """
        n = self.int_num_entries  # retrieve the number of entries
        # initialize the output object
        # initialize the bitarray for the valid entries
        ba_filter_of_selected_entries = bitarray(n)
        ba_filter_of_selected_entries.setall(
            0
        )  # an initialized output has no active entries

        # retrieve bitarray filter (or a filter of all active entries in the current layer)
        ba_filter = (
            self.filter
            if self.filter is not None
            else self.all(flag_return_valid_entries_in_the_currently_active_layer=True)
        )

        """ handle slices """
        if isinstance(l, slice):
            for i in bk.Slice_to_Range(l, n):
                if ba_filter[i]:
                    ba_filter_of_selected_entries[i] = True
            return ba_filter_of_selected_entries

        """ handle 'None' """
        if l is None:
            return ba_filter  # if None is given, return all active entries in the filter (or all active entries in the layer if a filter has not been set).

        """ handle a single value input """
        if not hasattr(l, "__iter__") or isinstance(
            l, str
        ):  # if a given input is not iterable or a string, wrap the element in a list
            l = [l]

        """ handle an empty list input """
        # handle empty inputs
        if len(l) == 0:
            return ba_filter_of_selected_entries  # return results

        """ handle string list input """
        if isinstance(l[0], str):  # when string representations were given
            flag_unload_str = (
                False  # a flag to unload string representations before exiting
            )
            # if str has not been loaded, load the data temporarily
            if self.map_str is None:
                flag_unload_str = True
                self.load_str()

            dict_mapping = self.map_str  # retrieve a dictionary for mapping str to int
            for e in l:
                if e in dict_mapping:
                    i = dict_mapping[e]
                    if ba_filter[
                        i
                    ]:  # if the entry is acitve in the filter (or filter objec containing all active entries)
                        ba_filter_of_selected_entries[i] = True

            # unload str data
            if flag_unload_str:
                self.unload_str()
            return ba_filter_of_selected_entries

        """ handle mask (bitarray / boolean array) """
        if len(l) == n and set(COUNTER(l[:10])).issubset(
            {0, 1, True, False}
        ):  # detect boolean array
            ba = self._convert_to_bitarray(l)  # convert mask to bitarray
            ba &= ba_filter  # apply filter
            return ba

        """ handle integer index list input """
        for i in l:
            if 0 <= i < n and ba_filter[i]:
                ba_filter_of_selected_entries[i] = True
        return ba_filter_of_selected_entries

    def save(self, path_folder, l_name_col: Union[None, list] = None):
        """# 2023-01-03 15:36:15
        save data contained in the Axis object (and metadata saved as ZarrDataFrame) to the new path.
        if a filter is active, filtered data will be saved.
        the number of entries in a chunk will be 'int_num_entries_in_a_chunk' attribute of the RamData

        'path_folder' : the path of the output Axis object
        'l_name_col' : the list of names of columns of the metadata to save. if None is given, all columns of the metadata will be saved
        """
        # retrieve attributes
        name_axis = self._name_axis

        # check validity of the path
        path_folder = (
            os.path.abspath(path_folder) + "/"
        )  # retrieve abspath of the output object
        assert self._path_folder != path_folder

        # create output folder
        filesystem_operations("mkdir", path_folder, exist_ok=True)

        """
        # save metadata
        """
        # save number and categorical data
        self.meta.save(
            f"{path_folder}{self._name_axis}.num_and_cat.zdf", l_name_col
        )  # save all columns

        """
        # save string data
        """
        # initialize
        za = zarr.open(
            f"{self._path_folder}{name_axis}.str.zarr",
            mode="r",
            synchronizer=zarr.ThreadSynchronizer(),
        )  # open a zarr object containing the string representation of the entries
        za_new = zarr.open(
            f"{path_folder}{name_axis}.str.zarr",
            mode="w",
            shape=(self.meta.n_rows, za.shape[1]),
            chunks=za.chunks,
            dtype=str,
            synchronizer=zarr.ThreadSynchronizer(),
        )  # writing a new zarr object

        int_size_buffer = (
            self.int_num_entries_in_a_chunk
        )  # use the chunk size as the size of the buffer
        ns = (
            dict()
        )  # namespace that can be safely modified across the scopes of the functions
        ns[
            "int_num_entries_written"
        ] = 0  # initialize the last position of written entries (after filter applied)
        ns[
            "int_num_bytes_written"
        ] = 0  # initialize the last position of written entries (after filter applied)
        ns["l_buffer"] = []  # initialize the buffer
        ns["flag_axis_initialized"] = False  # initialize the flag to False
        ns["index_chunk"] = 0  # initialize the index of the chunk

        def flush_buffer():
            """# 2022-07-04 23:34:40
            transfer string representations of entries to output str chunk object
            """
            # initialize str.chunks object
            if not ns["flag_axis_initialized"]:  # if the axis has not been initialized
                # create a folder to save a chunked string representations
                path_folder_str_chunks = f"{path_folder}{name_axis}.str.chunks/"
                filesystem_operations(
                    "mkdir", path_folder_str_chunks, exist_ok=True
                )  # create the output folder
                za_str_chunks = zarr.group(path_folder_str_chunks)
                ns["path_folder_str_chunks"] = path_folder_str_chunks
                za_str_chunks.attrs["dict_metadata"] = {
                    "int_num_entries": len(self),
                    "int_num_of_entries_in_a_chunk": self.int_num_entries_in_a_chunk,
                }  # write essential metadata for str.chunks
                ns["flag_axis_initialized"] = True  # set the flag to True

            # retrieve data of the entries in the buffer, and empty the buffer
            n = len(ns["l_buffer"])  # retrieve number of entries in the buffer
            data = za.get_orthogonal_selection(
                ns["l_buffer"]
            )  # retrieve data from the Zarr object
            ns["l_buffer"] = []  # empty the buffer

            # save str.chunks
            for index_col, arr_val in enumerate(data.T):
                with open(
                    f"{ns[ 'path_folder_str_chunks' ]}{ns[ 'index_chunk' ]}.{index_col}",
                    "wt",
                ) as newfile:  # similar organization to zarr
                    newfile.write(
                        base64_encode(gzip_bytes(("\n".join(arr_val) + "\n").encode()))
                    )
            ns["index_chunk"] += 1  # update 'index_chunk'

            # write Zarr object
            za_new[
                ns["int_num_entries_written"] : ns["int_num_entries_written"] + n, :
            ] = data  # transfer data to the new Zarr object
            ns["int_num_entries_written"] += n  # update the number of entries written

        # process entries using a buffer
        for i in (
            range(len(self)) if self.filter is None else BA.find(self.filter, val=1)
        ):  # iteratre through active integer representations of the entries
            ns["l_buffer"].append(i)
            if len(ns["l_buffer"]) >= int_size_buffer:  # flush the buffer if it is full
                flush_buffer()
        if len(ns["l_buffer"]) > 0:  # empty the buffer
            flush_buffer()

    def __repr__(self):
        """# 2022-07-20 23:12:47"""
        return f"<Axis '{self._name_axis}' containing {'' if self.filter is None else f'{self.meta.n_rows}/'}{self.meta._n_rows_unfiltered} entries available at {self._path_folder}\n\tavailable metadata columns are {sorted( self.columns )}>"

    def none(self):
        """# 2022-09-08 11:30:33
        return an empty bitarray filter
        """
        ba = bitarray(self.int_num_entries)
        ba.setall(0)
        return ba

    def exclude(self, filter_to_exclude):
        """# 2022-09-14 00:12:48
        exclude entries in the given filter 'filter_to_exclude' from the current filter
        """
        self.filter = self.filter & (
            ~filter_to_exclude
        )  # exclude the entries in 'filter_to_exclude'

    def all(
        self, flag_return_valid_entries_in_the_currently_active_layer: bool = False
    ):
        """# 2022-09-02 00:33:56
        return bitarray filter with all entries marked 'active'

        'flag_return_valid_entries_in_the_currently_active_layer' : return bitarray filter containing only the active entries in the current layer
        """

        if (
            flag_return_valid_entries_in_the_currently_active_layer
            and self._ramdata is not None
            and self._ramdata.layer is not None
            and self._ramdata.layer.get_ramtx(
                flag_is_for_querying_features=self._name_axis == "features"
            )
            is not None
        ):  # if RamData has an active layer and 'flag_return_valid_entries_in_the_currently_active_layer' setting is True, return bitarray where entries with valid count data is marked as '1' # if valid ramtx data is available
            rtx = self._ramdata.layer.get_ramtx(
                flag_is_for_querying_features=self._name_axis == "features"
            )  # retrieve associated ramtx object
            ba = rtx.ba_active_entries
            return ba
        else:
            # if layer is empty or 'flag_return_valid_entries_in_the_currently_active_layer' is False, just return a bitarray filled with '1'
            ba = bitarray(self.int_num_entries)
            ba.setall(1)  # set all entries as 'active'
            return ba  # return the bitarray filter

    def AND(self, *l_filter):
        """# 2022-06-27 21:37:31
        perform AND operations for the given list of filters (bitarray/np.ndarray objects)
        """
        if len(l_filter) == 0:
            return self.all()
        ba_result = self._convert_to_bitarray(l_filter[0])
        for ba in l_filter[1:]:
            ba_result &= self._convert_to_bitarray(ba)  # perform AND operation
        return ba_result  # return resulting filter

    def OR(self, *l_filter):
        """# 2022-06-28 20:16:42
        perform OR operations for the given list of filters (bitarray/np.ndarray objects)
        """
        if (
            len(l_filter) == 0
        ):  # if no inputs are given, return bitarray filter for all entries
            return self.all()
        ba_result = self._convert_to_bitarray(l_filter[0])
        for ba in l_filter[1:]:
            ba_result |= self._convert_to_bitarray(ba)  # perform OR operation
        return ba_result  # return resulting filter

    def NOT(self, filter=None):
        """# 2022-06-28 20:19:34
        reverse (not operation) the bitarray filter
        if no 'filter' is given, return empty bitarray
        """
        if filter is not None:
            ba = ~self._convert_to_bitarray(filter)  # perform 'not' operation
        else:
            ba = bitarray(self.int_num_entries)
            ba.setall(1)  # set all entries as 'active'
        return ba

    def XOR(self, filter_1, filter_2):
        """# 2022-06-28 20:24:20
        perform XOR operation between 'filter_1' and 'filter_2'
        """
        return self._convert_to_bitarray(filter_1) ^ self._convert_to_bitarray(filter_2)

    def batch_generator(
        self,
        ba=None,
        int_num_entries_for_batch: int = 1000,
        flag_mix_randomly: bool = False,
    ):
        """# 2022-07-16 22:57:23
        generate batches of list of integer indices of the active entries in the given bitarray 'ba'.
        Each bach has the following characteristics:
            monotonous: active entries in a batch are in an increasing order
            same size: except for the last batch, each batch has the same number of active entries 'int_num_entries_for_batch'.
        This function is simialr to RAMtx.batch_generator, except that the number of records for each entries ('weights') will not be considered when constructing a batch

        'ba' : (default None) if None is given, self.filter bitarray will be used.
        'flag_mix_randomly' : generate batches of entries after mixing randomly
        """
        # set defaule arguments
        # set default filter
        if ba is None:
            ba = self.ba_active_entries  # iterate through an active entries

        # initialize
        # a namespace that can safely shared between functions
        ns = {
            "index_batch": 0,
            "l_int_entry_current_batch": [],
            "int_num_of_previously_returned_entries": 0,
        }

        def __compose_batch():
            """# 2022-08-05 23:34:28
            compose batch from the values available in the namespace 'ns'
            """
            return {
                "index_batch": ns["index_batch"],
                "l_int_entry_current_batch": ns["l_int_entry_current_batch"],
                "int_num_of_previously_returned_entries": ns[
                    "int_num_of_previously_returned_entries"
                ],
            }

        if flag_mix_randomly:  # randomly select barcodes across the
            int_num_active_entries = (
                ba.count()
            )  # retrieve the total number of active entries
            float_ratio_batch_size_to_total_size = (
                int_num_entries_for_batch / int_num_active_entries
            )  # retrieve approximate number of batches to generate
            # initialize
            int_num_entries_added = 0
            ba_remaining = (
                ba.copy()
            )  # create a copy of the bitarray of active entries to mark the remaining entries
            float_prob_selection = int_num_entries_for_batch / max(
                1, int_num_active_entries - int_num_of_previously_returned_entries
            )  # calculate the initial probability for selection of entries
            while (
                int_num_entries_added < int_num_active_entries
            ):  # repeat entry selection process until all entries are selected
                for int_entry in BA.find(
                    ba_remaining
                ):  # iterate through remaining active entries
                    if (
                        np.random.random() < float_prob_selection
                    ):  # randomly make a decision whether to include the current entry or not
                        ns["l_int_entry_current_batch"].append(
                            int_entry
                        )  # collect 'int_entry' of the selected entry
                        ba_remaining[
                            int_entry
                        ] = False  # remove the entry from the 'ba_remaining' bitarray
                        int_num_entries_added += 1
                    # once the batch is full, yield the batch
                    if (
                        len(ns["l_int_entry_current_batch"])
                        >= int_num_entries_for_batch
                    ):
                        ns["l_int_entry_current_batch"] = np.sort(
                            ns["l_int_entry_current_batch"]
                        )  # sort the list of int_entries
                        yield __compose_batch()  # return batch
                        float_prob_selection = int_num_entries_for_batch / max(
                            1,
                            int_num_active_entries
                            - int_num_of_previously_returned_entries,
                        )  # update the probability for selection of an entry
                        ns["int_num_of_previously_returned_entries"] += len(
                            ns["l_int_entry_current_batch"]
                        )  # update the number of returned entries
                        ns[
                            "l_int_entry_current_batch"
                        ] = []  # initialize the next batch
                        ns["index_batch"] += 1
            # return the remaining int_entries as the last batch (if available)
            if len(ns["l_int_entry_current_batch"]) > 0:
                ns["l_int_entry_current_batch"] = np.sort(
                    ns["l_int_entry_current_batch"]
                )  # sort the list of int_entries
                yield __compose_batch()  # return batch
        else:  # return barcodes in a batch sequentially
            for int_entry in BA.find(
                ba
            ):  # iterate through active entries of the given bitarray
                ns["l_int_entry_current_batch"].append(
                    int_entry
                )  # collect int_entry for the current batch
                # once the batch is full, yield the batch
                if len(ns["l_int_entry_current_batch"]) >= int_num_entries_for_batch:
                    yield __compose_batch()  # return batch
                    ns["int_num_of_previously_returned_entries"] += len(
                        ns["l_int_entry_current_batch"]
                    )  # update the number of returned entries
                    ns["l_int_entry_current_batch"] = []  # initialize the next batch
                    ns["index_batch"] += 1
            # return the remaining int_entries as the last batch (if available)
            if len(ns["l_int_entry_current_batch"]) > 0:
                yield __compose_batch()  # return batch

    def change_filter(self, name_col_filter: str):
        """# 2022-07-16 17:17:29
        change filter using the filter saved in the metadata with 'name_col_filter' column name. if 'name_col_filter' is not available, current filter setting will not be changed.

        'name_col_filter' : name of the column of the metadata ZarrDataFrame containing the filter
        """
        if (
            name_col_filter in self.meta
        ):  # if a given column name exists in the current metadata ZarrDataFrame
            self.filter = self.meta[
                name_col_filter, :
            ]  # retrieve filter from the storage and apply the filter to the axis

    def get_filter(self, name_col_filter: str):
        """# 2023-02-09 22:13:51
        convenience function for load and get a filter

        'name_col_filter' : name of the column of the metadata ZarrDataFrame containing the filter
        """
        return self._convert_to_bitarray(
            self.meta[name_col_filter, :]
            if name_col_filter in self.meta
            else self.none()
        )  # if a given column name does not exist in the current metadata ZarrDataFrame, return an empty filter

    def save_filter(
        self,
        name_col_filter: str,
        dict_col_metadata_description: Union[None, dict] = {
            "intended_function": "filter"
        },
    ):
        """# 2022-12-05 11:57:32
        save current filter using the filter to the metadata with 'name_col_filter' column name. if a filter is not active, the metadata will not be updated.

        'name_col_filter' : name of the column of the metadata ZarrDataFrame that will contain the filter
        'dict_col_metadata_description' : description about the column. Set to None to omit a description about the column
        """
        self.save_as_filter(
            self.filter,
            name_col_filter=name_col_filter,
            dict_col_metadata_description=dict_col_metadata_description,
        )

    def save_as_filter(
        self,
        ba_filter,
        name_col_filter: str,
        dict_col_metadata_description: Union[None, dict] = {
            "intended_function": "filter"
        },
    ):
        """# 2023-01-17 18:27:01
        save current filter using the filter to the metadata with 'name_col_filter' column name. if a filter is not active, the metadata will not be updated.

        ba_filter # an array (bitarray, boolean array, l_int_indices) containing the active entries of the current axis
        'name_col_filter' : name of the column of the metadata ZarrDataFrame that will contain the filter
        'dict_col_metadata_description' : description about the column. Set to None to omit a description about the column
        """
        if name_col_filter is not None:  # if a given filter name is valid
            self.meta[name_col_filter, :] = BA.to_array(
                self._convert_to_bitarray(ba_filter)
            )  # save filter to the storage # when a filter is not active, save filter of all active entries of the RAMtx
            # update description metadata for the column
            if (
                dict_col_metadata_description is not None
            ):  # if valid 'dict_col_metadata_description' has been given
                self.meta.set_column_metadata_description(
                    name_col_filter, dict_col_metadata_description
                )  # update description metadata for the column

    def change_or_save_filter(
        self,
        name_col_filter: str,
        dict_col_metadata_description: Union[None, dict] = {
            "intended_function": "filter"
        },
    ):
        """# 2022-12-05 11:49:14
        change filter to 'name_col_filter' if 'name_col_filter' exists in the metadata, or save the currently active entries (filter) to the metadata using the name 'name_col_filter'

        'name_col_filter' : name of the column of the metadata ZarrDataFrame that will contain the filter
        'dict_col_metadata_description' : description about the column. Set to None to omit a description about the column
        """
        if name_col_filter is not None:  # if valid 'name_col_filter' has been given
            if name_col_filter in self.meta:
                self.change_filter(
                    name_col_filter
                )  # change filter to 'name_col_filter' if 'name_col_filter' exists in the metadata
            else:
                self.save_filter(
                    name_col_filter,
                    dict_col_metadata_description=dict_col_metadata_description,
                )  # save the currently active entries (filter) to the metadata ZDF using the name 'name_col_filter'

    def subsample(
        self,
        float_prop_subsampling: float = 1,
        ba_to_subsample: Union[None, bitarray] = None,
    ):
        """# 2023-03-11 21:42:54
        subsample active entries in the current filter (or all the active entries with valid data) using the proportion of subsampling ratio 'float_prop_subsampling'

        ba_to_subsample : Union[ None, bitarray ] = None # a filter (bitarray) object to subsample. if None is given, current filter will be used for subsampling.
        """
        # if 'ba_to_subsample' is None, retrieve bitarray of active entries by default
        if ba_to_subsample is None:
            ba_to_subsample = self.ba_active_entries

        # return the bitarray of all active entries if no subsampling is required
        if float_prop_subsampling is None or float_prop_subsampling == 1:
            return ba_to_subsample

        # initialize the output bitarray filter that will contain subsampled entries
        ba_subsampled = bitarray(self.int_num_entries)
        ba_subsampled.setall(0)  # exclude all entries by default

        # perform subsampling
        for int_entry in BA.find(ba_to_subsample):
            if np.random.random() < float_prop_subsampling:
                ba_subsampled[int_entry] = True

        # return subsampled entries
        return ba_subsampled

    def select_component(self, int_index_component: int = 0, inplace: bool = False):
        """# 2023-02-26 15:54:33
        return a filter containing entries of the selected component.
        if current RamData does not have any component, return all entries of the current axis.

        int_index_component : int = 0 # the integer index of the component (0-based)
        inplace : bool = False # if True, set the filter of the current axis using the returned values.
        """
        if self.is_combined:
            # handle invalid input
            if (
                int_index_component >= self.n_components or int_index_component < 0
            ):  # check validity of the input component index
                int_index_component = (
                    0  # set default component when invalid input is used
                )
            # initialize an empty filter
            ba = bitarray(self.int_num_entries)
            ba.setall(0)
            # select the entries of the selected component
            if (
                self.is_interleaved
            ):  # when 'combined-interleaved' mode is active, iterate over entries of the combined axis present in the component axis.
                for (
                    int_entry_combined
                ) in self._l_dict_index_mapping_from_combined_to_component[
                    int_index_component
                ]:
                    ba[int_entry_combined] = 1
            else:  # when 'combined-stacked' mode is active
                ba[
                    self._l_cumulated_len_stacked[
                        int_index_component
                    ] : self._l_cumulated_len_stacked[int_index_component + 1]
                ] = 1
        else:  # if current axis is not in 'combined' mode, return a filter containing all entries
            ba = self.all(flag_return_valid_entries_in_the_currently_active_layer=False)
        # process the output
        if inplace:
            self.filter = ba  # set the filter of the current component.
        else:
            return ba  # return filter containing the selection

    @property
    def is_destination_component_set(self):
        """# 2022-09-21 02:18:13
        return True if a destination component has been set
        """
        return self._int_index_component_destination is not None

    def set_destination_component(self, index_component: Union[None, int] = None):
        """# 2022-09-20 18:27:22
        set_destination_component

        index_component : Union[ None, int ] = None : the index of a destination component
        """
        if (
            self.is_combined
        ):  # only set destination component when current axis is using 'combined' mode
            if index_component is not None:  # set destination component
                # check validity of input
                if not (0 <= index_component < self.n_components):
                    index_component = 0  # set default 'index_component' if the component 'index_component' is not valid
                self._dict_index_mapping_from_combined_to_dest_component = (
                    self._l_dict_index_mapping_from_combined_to_component[
                        index_component
                    ]
                )
                self._int_index_component_destination = index_component
            else:  # reset destination component
                self._dict_index_mapping_from_combined_to_dest_component = None
                self._int_index_component_destination = None

    def update(self, df):
        """# 2022-10-29 18:13:15
        update metadata using the given dataframe, whose indices is either the string or integer representations of the entries
        """
        # check whether the input is valid datatype
        if not isinstance(df, pd.DataFrame):
            return
        if len(df) == 0:  # exit if an empty dataframe has been given
            return
        if len(df.columns.values) == 0:  # exit if no columns exist in the dataframe
            return
        # retrieve a flag indicating whether the string representations were used
        flag_str_repr_was_used = isinstance(df.index.values[0], str)
        flag_str_repr_was_loaded = (
            self.flag_str_repr_loaded
        )  # retrieve a flag indicating whether the string representations were loaded at the time when the function was called

        # map string representations to the integer representations of the entries
        # %% STRING REPR. %%
        if flag_str_repr_was_used:
            # load string representations
            if not flag_str_repr_was_loaded:
                self.load_str()

            # map string representations to the integer representations of the entries
            l_int_entry = []
            l_mask_mapped_to_int_entry = []
            dict_map_str = self.map_str  # retrieve mapping
            for e in df.index.values:
                if e in dict_map_str:
                    l_int_entry.append(dict_map_str[e])
                    l_mask_mapped_to_int_entry.append(True)
                else:
                    l_mask_mapped_to_int_entry.append(False)

            # exclude entries whose string representations cannot be mapped to the string representations loaded in the current axis object
            if np.sum(l_mask_mapped_to_int_entry) < len(df):
                df = df[l_mask_mapped_to_int_entry]
            df.index = l_int_entry  # convert index entries fro string representations to integer representations of the entries

        # update the metadata
        self.meta.update(df, flag_use_index_as_integer_indices=True)

        # unload string representations
        if flag_str_repr_was_used and not flag_str_repr_was_loaded:
            self.unload_str()

    def get_df(self, *l_name_col):
        """# 2022-10-29 22:47:00
        retrieve metadata of a given list of columns as a dataframe
        """
        # retrieve dataframe from the metadata zdf
        df = self.meta.get_df(*l_name_col)
        if df is None:  # when no data could be retrieved, exit
            return

        # retrieve string representations (if string repr. have been already loaded)
        if self.flag_str_repr_loaded:  # if string repr. have been already loaded
            dict_map_int = self.map_int  # retrieve mapping
            df.index = list(
                dict_map_int[e] if e in dict_map_int else e for e in df.index.values
            )  # map integer representations to string representations
        return df

    @property
    def filters(self, flag_excluding_components: bool = False):
        """# 2023-02-14 23:26:09
        convenience funciton
        list the name of the columns that contains filters, according to the column metadata.

        flag_excluding_components : bool = False # exclude the columns in the component axes
        """
        metadata_columns = (
            self.meta.metadata_columns_excluding_components
            if flag_excluding_components
            else self.meta.metadata_columns
        )  # retrieve 'metadata_columns'

        l_name_col = list()  # initialize the list
        for name_col in metadata_columns:
            dict_meta = metadata_columns[
                name_col
            ]  # retrieve metadata of the current column
            if isinstance(dict_meta, dict) and "intended_function" in dict_meta:
                if dict_meta["intended_function"] == "filter":
                    l_name_col.append(name_col)
        return sorted(
            l_name_col
        )  # return the sorted list of name of the columns containing filters

    def search_columns(self, *args, **kwargs):
        """# 2023-03-05 19:14:17
        search columns of the metadata ZarrDataFrame
        """
        return self.meta.search_columns(*args, **kwargs)


""" a class for RAMtx """
""" a class for accessing Zarr-backed count matrix data (RAMtx, Random-Access matrix) """


class RAMtx:
    """# 2023-02-26 22:33:17
    This class represent a random-access mtx format for memory-efficient exploration of extremely large single-cell transcriptomics/genomics data.
    This class use a count matrix data stored in a random read-access compatible format, called RAMtx, enabling exploration of a count matrix with hundreds of millions cells with hundreds of millions of features.
    Also, the RAMtx format is supports multi-processing, and provide convenient interface for parallel processing of single-cell data
    Therefore, for exploration of count matrix produced from 'scarab count', which produces dozens of millions of features extracted from both coding and non coding regions, this class provides fast front-end application for exploration of exhaustive data generated from 'scarab count'


    # 'mode' of RAMtx objects
    There are three valid 'mode' (or internal structures) for RAMtx object : {'dense' or 'sparse_for_querying_barcodes', 'sparse_for_querying_features'}

    (sparse_for_querying_barcodes) <---> (dense) <---> (sparse_for_querying_features)
    *fast barcode data retrieval                       *fast feature data retrieval

    As shown above, RAMtx objects are interconvertible. Of note, for the converion between sparse ramtx sorted by barcodes and features, 'dense' ramtx object should be used in the conversion process.
    - dense ramtx object can be used to retrieve data of a single barcode or feature (with moderate efficiency)
    - sparse ramtx object can only be used data of either a single barcode ('sparse_for_querying_barcodes') or a single feature ('sparse_for_querying_features') very efficiently.

    # 2022-08-30 11:44:49
    'combined' mode was initialized.

    arguments:
    'path_folder_ramtx' : a folder containing RAMtx object
    'ba_filter_features' : a bitarray filter object for features. active element is marked by 1 and inactive element is marked by 0
    'ba_filter_barcodes' : a bitarray filter object for barcodes. active element is marked by 1 and inactive element is marked by 0
    'dtype_of_feature_and_barcode_indices' : dtype of feature/barcode indices
    'dtype_of_values' : dtype of values.
    'int_num_cpus' : the number of processes that will be used for random accessing of the data
    'mode' : file mode. 'r' for read-only mode and 'a' for a mode allowing modifications
    'flag_is_read_only' : read-only status of RamData
    'path_folder_ramtx_mask' : a local (local file system) path to the mask of the RAMtx object that allows modifications to be written without modifying the source. if a valid local path to a mask is given, all modifications will be written to the mask
    'is_for_querying_features' : a flag for indicating whether the current RAMtx will be used for querying features. for sparse matrix, this attribute will be fixed. However, for dense matrix, this atrribute can be changed any time.
    'int_total_number_of_values_in_a_batch_for_dense_matrix' : the total number of values that will be loaded in dense format for each minibatch (subbatch) when retrieving sparse data from the dense matrix using multiple number of processes. this setting can be changed later
    'rtx_template' : a RAMtx object to use as a template (copy arguments except for 'l_rtx', 'rtx_template', 'flag_spawn')
    'flag_spawn' : if True, use zarr server with a spawned process to perform zarr operations. When multiprocessing using forked processes is used, zarr operations that are not fork-safe should be performed within a spawned process.

    === arguments for combined RAMtx ===
    'l_rtx' : list of component RAMtx object for the 'combined' mode. to disable 'combined' mode, set this argument to None

    === arguments for component RAMtx ===
    dict_index_mapping_from_component_to_combined_bc : mapping dictionary-like object.
    dict_index_mapping_from_component_to_combined_ft : mapping dictionary-like object.
    dict_index_mapping_from_combined_to_component_bc : mapping dictionary-like object.
    dict_index_mapping_from_combined_to_component_ft : mapping dictionary-like object.
    dict_index_mapping_from_combined_to_dest_component_ft : mapping dictionary-like object.
    dict_index_mapping_from_combined_to_dest_component_bc : mapping dictionary-like object.

    === Synchronization across multiple processes ===
    zarrspinlockserver : Union[ None, ZarrSpinLockServer ] = None # a ZarrSpinLockServer object for synchronization of methods of the current object.
    """

    def __init__(
        self,
        path_folder_ramtx=None,
        l_rtx: Union[list, tuple, None] = None,
        dict_index_mapping_from_component_to_combined_bc: Union[dict, None] = None,
        dict_index_mapping_from_component_to_combined_ft: Union[dict, None] = None,
        dict_index_mapping_from_combined_to_component_bc: Union[dict, None] = None,
        dict_index_mapping_from_combined_to_component_ft: Union[dict, None] = None,
        ramdata=None,
        dtype_of_feature_and_barcode_indices=np.uint32,
        dtype_of_values=np.float64,
        int_num_cpus: int = 1,
        verbose: bool = False,
        flag_debugging: bool = False,
        mode: str = "a",
        flag_is_read_only: bool = False,
        path_folder_ramtx_mask: Union[str, None] = None,
        is_for_querying_features: bool = True,
        int_total_number_of_values_in_a_batch_for_dense_matrix: int = 10000000,
        rtx_template=None,
        flag_spawn=False,
        zarrspinlockserver: Union[None, ZarrSpinLockServer] = None,
    ):
        """# 2023-02-27 20:51:21"""
        if (
            rtx_template is not None
        ):  # when template has been given, copy attributes and metadata
            # set attributes based on the given template
            self._path_folder_ramtx = rtx_template._path_folder_ramtx
            self._dict_index_mapping_from_component_to_combined_bc = (
                rtx_template._dict_index_mapping_from_component_to_combined_bc
            )
            self._dict_index_mapping_from_component_to_combined_ft = (
                rtx_template._dict_index_mapping_from_component_to_combined_ft
            )
            self._dict_index_mapping_from_combined_to_component_bc = (
                rtx_template._dict_index_mapping_from_combined_to_component_bc
            )
            self._dict_index_mapping_from_combined_to_component_ft = (
                rtx_template._dict_index_mapping_from_combined_to_component_ft
            )
            self._ramdata = rtx_template._ramdata
            self._dtype_of_feature_and_barcode_indices = (
                rtx_template._dtype_of_feature_and_barcode_indices
            )
            self._dtype_of_values = rtx_template._dtype_of_values
            self.verbose = rtx_template.verbose
            self.flag_debugging = rtx_template.flag_debugging
            self._mode = rtx_template._mode
            self._flag_is_read_only = rtx_template._flag_is_read_only
            self._path_folder_ramtx_mask = rtx_template._path_folder_ramtx_mask
            self._is_for_querying_features = rtx_template._is_for_querying_features
            self.int_total_number_of_values_in_a_batch_for_dense_matrix = (
                rtx_template.int_total_number_of_values_in_a_batch_for_dense_matrix
            )

            # set read-only attributes
            self._flag_spawn = flag_spawn

            # set metadata (avoid further zarr operation)
            self._root = rtx_template._root
            self._dict_metadata = rtx_template._dict_metadata

            # set 'l_rtx'
            self._l_rtx = l_rtx

            # load a zarr spin lock server
            self._zsls = rtx_template._zsls

            # set attributes
            self.int_num_cpus = rtx_template.int_num_cpus
        else:
            # set attributes
            self._dtype_of_feature_and_barcode_indices = (
                dtype_of_feature_and_barcode_indices
            )
            self._dtype_of_values = dtype_of_values
            self._path_folder_ramtx = path_folder_ramtx
            self.verbose = verbose
            self.flag_debugging = flag_debugging
            self._ramdata = ramdata
            self._mode = mode
            self._flag_is_read_only = flag_is_read_only
            self._path_folder_ramtx_mask = path_folder_ramtx_mask
            self.int_total_number_of_values_in_a_batch_for_dense_matrix = (
                int_total_number_of_values_in_a_batch_for_dense_matrix
            )
            self._l_rtx = l_rtx
            # set read-only attributes
            self._flag_spawn = flag_spawn
            # mapping dictionaries
            self._dict_index_mapping_from_component_to_combined_bc = (
                dict_index_mapping_from_component_to_combined_bc
            )
            self._dict_index_mapping_from_component_to_combined_ft = (
                dict_index_mapping_from_component_to_combined_ft
            )
            self._dict_index_mapping_from_combined_to_component_ft = (
                dict_index_mapping_from_combined_to_component_ft
            )
            self._dict_index_mapping_from_combined_to_component_bc = (
                dict_index_mapping_from_combined_to_component_bc
            )

            # load a zarr spin lock server
            self._zsls = (
                zarrspinlockserver
                if isinstance(zarrspinlockserver, ZarrSpinLockServer)
                else None
            )

            # set attributes
            self.int_num_cpus = int_num_cpus

            # compose metadata for the combined ramtx
            # %% COMBINED %%
            if self.is_combined:
                """write metadata"""
                if not zarr_exists(path_folder_ramtx):
                    if self.use_locking:  # %% FILE LOCKING %%
                        self._zsls.acquire_lock(f"{path_folder_ramtx}.zattrs.lock")

                    self._root = zarr.open(path_folder_ramtx, "a")
                    # compose metadata
                    self._dict_metadata = {
                        "path_folder_mtx_10x_input": None,
                        "mode": "___".join(
                            list("None" if rtx is None else rtx.mode for rtx in l_rtx)
                        ),  # compose mode
                        "str_completed_time": bk.TIME_GET_timestamp(True),
                        "int_num_features": ramdata.ft.int_num_entries,  # use the number of entries of the combined RamData
                        "int_num_barcodes": ramdata.bc.int_num_entries,  # use the number of entries of the combined RamData
                        "int_num_records": sum(
                            rtx._int_num_records for rtx in l_rtx if rtx is not None
                        ),  # calculate the total number of records
                        "version": _version_,
                    }
                    self._root.attrs[
                        "dict_metadata"
                    ] = self._dict_metadata  # write the metadata

                    if self.use_locking:  # %% FILE LOCKING %%
                        self._zsls.release_lock(f"{path_folder_ramtx}.zattrs.lock")

                # set component indices mapping dictionaries
                for (
                    rtx,
                    dict_index_mapping_from_component_to_combined_bc,
                    dict_index_mapping_from_component_to_combined_ft,
                    dict_index_mapping_from_combined_to_component_bc,
                    dict_index_mapping_from_combined_to_component_ft,
                ) in zip(
                    l_rtx,
                    ramdata.bc._l_dict_index_mapping_from_component_to_combined,
                    ramdata.ft._l_dict_index_mapping_from_component_to_combined,
                    ramdata.bc._l_dict_index_mapping_from_combined_to_component,
                    ramdata.ft._l_dict_index_mapping_from_combined_to_component,
                ):
                    if rtx is not None:
                        # set mapping dictionaries to each rtx component
                        rtx._dict_index_mapping_from_component_to_combined_ft = (
                            dict_index_mapping_from_component_to_combined_ft
                        )
                        rtx._dict_index_mapping_from_component_to_combined_bc = (
                            dict_index_mapping_from_component_to_combined_bc
                        )
                        rtx._dict_index_mapping_from_combined_to_component_ft = (
                            dict_index_mapping_from_combined_to_component_ft
                        )
                        rtx._dict_index_mapping_from_combined_to_component_bc = (
                            dict_index_mapping_from_combined_to_component_bc
                        )
            # read metadata
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.wait_lock(f"{path_folder_ramtx}.zattrs.lock")
            self._root = zarr.open(path_folder_ramtx, "a")
            self._dict_metadata = self._root.attrs[
                "dict_metadata"
            ]  # retrieve the metadata

        # parse the metadata of the RAMtx object
        self._int_num_features, self._int_num_barcodes, self._int_num_records = (
            self._dict_metadata["int_num_features"],
            self._dict_metadata["int_num_barcodes"],
            self._dict_metadata["int_num_records"],
        )

        # set filters using RamData
        self.ba_filter_features = (
            self._ramdata.ft.filter if self._ramdata is not None else None
        )
        self.ba_filter_barcodes = (
            self._ramdata.bc.filter if self._ramdata is not None else None
        )

        # load zarr objects, a file system server, and settings required for RAMtx operations
        if not self.is_combined:
            # open zarr objects
            self._is_sparse = (
                self.mode != "dense"
            )  # retrieve a flag indicating whether ramtx is dense
            if self.is_sparse:
                self._is_for_querying_features = self._dict_metadata[
                    "flag_ramtx_sorted_by_id_feature"
                ]  # for sparse matrix, this attribute is fixed
                # open Zarr object containing matrix and matrix indices
                self._za_mtx_index = ZarrServer(
                    f"{self._path_folder_ramtx}matrix.index.zarr",
                    "r",
                    flag_spawn=flag_spawn,
                )
                self._za_mtx = ZarrServer(
                    f"{self._path_folder_ramtx}matrix.zarr", "r", flag_spawn=flag_spawn
                )
            else:  # dense matrix
                self.is_for_querying_features = (
                    is_for_querying_features  # set this attribute
                )
                self._za_mtx = ZarrServer(
                    f"{self._path_folder_ramtx}matrix.zarr", "r", flag_spawn=flag_spawn
                )
        else:
            # %% COMBINED %%
            self._is_sparse = None
            self._za_mtx = None
            self._is_for_querying_features = list(
                rtx for rtx in l_rtx if rtx is not None
            )[
                0
            ].is_for_querying_features  # use 'is_for_querying_features' of the first valid RAMtx component
        # attach a file system server
        self.fs = FileSystemServer(flag_spawn=flag_spawn)

        # if 'flag_spawn' is True, start the new 'ZarrSpinLockServer' object with spawned processes
        if flag_spawn:
            self._zsls = ZarrSpinLockServer(
                flag_spawn=flag_spawn, filesystem_server=self.fs, template=self._zsls
            )

    @property
    def path_folder(self):
        """# 2023-04-12 17:19:28"""
        return self._path_folder_ramtx

    @property
    def int_num_cpus(self):
        """# 2023-02-27 20:50:10
        number of cpu cores to use for RamData and RamDataAxis operations
        """
        return self._int_num_cpus

    @int_num_cpus.setter
    def int_num_cpus(self, val):
        """# 2023-02-27 20:50:04
        change the number of cpu cores to use for RamData and RamDataAxis operations
        """
        self._int_num_cpus = val
        # %% COMBINED %%
        if (
            self.is_combined
        ):  # propagate the change of 'int_num_cpus' to the component RamData objects.
            for rtx in self._l_rtx:
                if rtx is not None:
                    rtx.int_num_cpus = val

    @property
    def locking_server(self):
        """# 2022-12-23 00:02:37
        return 'ZarrSpinLockServer' object
        """
        return self._zsls

    @locking_server.setter
    def locking_server(self, locking_server_new):
        """# 2022-12-23 00:02:43"""
        self._zsls = (
            locking_server_new  # set 'ZarrSpinLockServer' of the current object
        )

    @property
    def flag_spawn(self):
        """# 2022-12-06 02:37:31
        return a flag indicating spawning should be used for operations that might not be fork-safe
        """
        return self._flag_spawn

    @property
    def contains_remote(self):
        """# 2022-09-05 17:55:26
        return True if current RAMtx is in remote location or contains component RAMtx hosted remotely
        """
        # if current RAMtx is in remote location, return True
        if self.is_remote:
            return True
        # if current RAMtx is in combined mode, survey its component and identify ramtx located remotely
        if self.is_combined:
            for rtx in self._l_rtx:
                if rtx is not None and rtx.is_remote:
                    return True

    @property
    def is_remote(self):
        """# 2022-09-03 17:17:32
        return True if the RAMtx is located remotely
        """
        return is_remote_url(self._path_folder_ramtx)

    def get_fork_safe_version(self):
        """# 2022-12-05 23:57:20
        return RAMtx object that are fork-safe.
        replace zarr objects with zarr_server objects if current RAMtx object is located remotely
        """
        rtx_with_zarr_server = self  # by default, current RAMtx object as-is
        # for remote zarr object, load the zarr object using the ZarrServer to avoid fork-not-safe error
        if self.contains_remote:
            if not self.is_combined:
                # for remote zarr object, load the zarr object in a spawned process using the ZarrServer to avoid fork-not-safe error
                rtx_with_zarr_server = (
                    RAMtx(rtx_template=self, flag_spawn=True)
                    if self.is_remote
                    else self
                )
            else:
                # load zarr server for each component RAMtx object
                rtx_with_zarr_server = RAMtx(
                    rtx_template=self,
                    l_rtx=list(
                        None if rtx is None else rtx.get_fork_safe_version()
                        for rtx in self._l_rtx
                    ),
                )
        return rtx_with_zarr_server

    def terminate_spawned_processes(self):
        """# 2023-02-26 22:33:09
        destroy zarr server objects if they exists in the current RAMtx
        """
        if not hasattr(
            self, "_flag_is_terminated"
        ):  # terminate the spawned processes only once
            # terminate the file system server
            self.fs.terminate()
            # for remote zarr object, terminate the servers for each component
            if (
                not self.is_combined and self.is_remote
            ):  # if current RAMtx is remotely located
                if self.is_sparse:
                    # destroy Zarr object hosted in a spawned process
                    if hasattr(self._za_mtx_index, "terminate"):
                        self._za_mtx_index.terminate()
                    if hasattr(self._za_mtx, "terminate"):
                        self._za_mtx.terminate()
                else:  # dense matrix
                    if hasattr(self._za_mtx, "terminate"):
                        self._za_mtx.terminate()
                if self.use_locking:  # %% FILE LOCKING %%
                    self._zsls.terminate()  # termiate the locking server
            elif self.is_combined:
                # %% COMBINED %%
                # destroy zarr server for each component RAMtx object
                for rtx in self._l_rtx:
                    if rtx is not None:
                        rtx.terminate_spawned_processes()
            self._flag_is_terminated = (
                True  # set a flag indicating spawned processes have been terminated.
            )

    def get_za(self):
        """# 2022-09-05 11:11:05
        get zarr objects for operating RAMtx matrix.  the primary function of this function is to retrieve a zarr objects hosted in a thread-safe spawned process when the source is remotely located (http)
        """
        # retrieve zarr object for index and matrix
        za_mtx_index, za_mtx = None, None
        if not self.is_combined:
            # open zarr objects
            self._is_sparse = (
                self.mode != "dense"
            )  # retrieve a flag indicating whether ramtx is dense
            if self.is_sparse:
                # open Zarr object containing matrix and matrix indices
                za_mtx_index = self._za_mtx_index
                za_mtx = self._za_mtx
            else:  # dense matrix
                za_mtx = self._za_mtx
        return za_mtx_index, za_mtx

    @property
    def is_component(self):
        """# 2022-08-30 11:46:15
        return True if current RAMtx is one of the components of a combined RAMtx object
        """
        return not (
            self._dict_index_mapping_from_component_to_combined_ft is None
            or self._dict_index_mapping_from_component_to_combined_bc is None
        )

    @property
    def is_combined(self):
        """# 2022-08-30 11:46:15
        return True if current RAMtx is in 'combined' mode
        """
        return self._l_rtx is not None

    @property
    def is_sparse(self):
        """# 2022-08-04 13:59:15"""
        return self._is_sparse

    @property
    def mode(self):
        """# 2022-07-30 20:13:32"""
        return self._dict_metadata["mode"]

    @property
    def _path_folder_ramtx_modifiable(self):
        """# 2022-07-21 09:04:28
        return the path to the modifiable RAMtx object
        """
        return (
            (None if self._flag_is_read_only else self._path_folder_ramtx)
            if self._path_folder_ramtx_mask is None
            else self._path_folder_ramtx_mask
        )

    @property
    def ba_active_entries(self):
        """# 2022-12-02 21:39:31
        return a bitarray filter of the indexed axis where all the entries with valid count data is marked '1'
        """
        # initialize
        flag_spawn = self.flag_spawn

        # retrieve axis of current ramtx
        axis = "features" if self.is_for_querying_features else "barcodes"

        # skip if result is already available
        flag_available = False  # initialize
        for path_folder in [
            self._path_folder_ramtx,
            self._path_folder_ramtx_modifiable,
        ]:
            if path_folder is not None and zarr_exists(
                f"{path_folder}matrix.{axis}.active_entries.zarr/",
                filesystemserver=self.fs,
            ):
                path_folder_zarr = f"{path_folder}matrix.{axis}.active_entries.zarr/"  # define an existing zarr object path
                flag_available = True
        if (
            not flag_available and self._path_folder_ramtx_modifiable is not None
        ):  # if zarr object does not exists and modifiable ramtx path is available
            # try constructing the zarr object
            path_folder_zarr = f"{self._path_folder_ramtx_modifiable}matrix.{axis}.active_entries.zarr/"  # define zarr object path
            self.survey_number_of_records_for_each_entry()  # survey the number of records for each entry using default settings
            if zarr_exists(
                path_folder_zarr, filesystemserver=self.fs
            ):  # if the zarr object is available, set 'flag_available' to True
                flag_available = True

        if not flag_available:  # if the zarr object still does not exists
            logger.warning(
                f"'ba_active_entries' of axis '{axis}' for {self._path_folder_ramtx} RAMtx cannot be retrieved. as a fallback, a filter of all entries will be returned."
            )
            # create a full bitarray mask as a fallback
            ba = bitarray(self.len_axis_for_querying)
            ba.setall(1)
            return ba

        za = ZarrServer(
            path_folder_zarr, mode="r", flag_spawn=flag_spawn
        )  # open zarr object of the current RAMtx object
        ba = BA.to_bitarray(
            za[:]
        )  # return the boolean array of active entries as a bitarray object

        # if metadata of the number of active entries is not available, update the metadata
        if "n_active_entries" in self._dict_metadata:
            self._n_active_entries = (
                ba.count()
            )  # calculate the number of active entries

            # update metadata
            self._dict_metadata["n_active_entries"] = self._n_active_entries
            self._save_metadata_()

        # terminate the spawned processes
        za.terminate()
        # return the mask
        return ba

    def _get_path_folder_number_of_records_for_each_entry(
        self, axis: Literal["barcodes", "features"]
    ):
        """# 2022-08-31 13:55:13
        return path of the folder where number of records for each entry resides for the given entry.
        if the records are not available, None will be returned.
        """
        # skip if result is already available
        flag_res_available = False  # initialize
        for path_folder in [
            self._path_folder_ramtx,
            self._path_folder_ramtx_modifiable,
        ]:
            if path_folder is not None and zarr_exists(
                f"{path_folder}matrix.{axis}.number_of_records_for_each_entry.zarr/",
                filesystemserver=self.fs,
            ):
                flag_res_available = True
                break
        return (
            path_folder if flag_res_available else None
        )  # if result is not available, returns None. if result is available, return the folder where the result reside

    def survey_number_of_records_for_each_entry(
        self,
        axes=["barcodes", "features"],
        int_num_chunks_in_a_batch_for_index_of_sparse_matrix=100,
        int_num_chunks_in_a_batch_for_axis_for_querying_dense=1,
        int_total_number_of_values_in_a_batch_for_dense_matrix=None,
        int_size_chunk=1000,
        flag_ignore_dense=False,
        int_num_threads=20,
    ):
        """# 2022-12-06 19:18:44
        survey the number of records for each entry in the existing axis
        'axes' : a list of axes to use for surveying the number of records for each entry

        === batch size control ===
        'int_num_chunks_in_a_batch_for_index_of_sparse_matrix' : the number of chunks of the index zarr object to be processed once for sparse matrix RAMtx formats
        'int_num_chunks_in_a_batch_for_axis_for_querying_dense' : the number of chunks in the axis for the axis for querying that will be processed together in a batch for each process
        'int_total_number_of_values_in_a_batch_for_dense_matrix' : the total number of values that will be loaded during the suvery for each process for surveying dense matrix with multiple number of processes.

        'int_size_chunk' : chunk size for the output zarr objects
        'flag_ignore_dense' : if True, does not survey the dense ramtx.
        'int_num_threads' : the number of threads for surveying
        """
        # initialize
        flag_spawn = self.flag_spawn

        # handle combined mode - run 'survey_number_of_records_for_each_entry' in the components
        if self.is_combined:
            # %% COMBINED %%
            # drop the RAMtx object of the reference if combined and reference alignment modes are active
            self.drop_reference()

            # (run the current function in individual ramdata)
            for rtx in self._l_rtx:
                if rtx is None:
                    continue
                rtx.survey_number_of_records_for_each_entry(
                    axes=axes,
                    int_num_chunks_in_a_batch_for_index_of_sparse_matrix=int_num_chunks_in_a_batch_for_index_of_sparse_matrix,
                    int_num_chunks_in_a_batch_for_axis_for_querying_dense=int_num_chunks_in_a_batch_for_axis_for_querying_dense,
                    int_total_number_of_values_in_a_batch_for_dense_matrix=int_total_number_of_values_in_a_batch_for_dense_matrix,
                    int_size_chunk=int_size_chunk,
                    flag_ignore_dense=flag_ignore_dense,
                    int_num_threads=int_num_threads,
                )

        # use default value when 'int_total_number_of_values_in_a_batch_for_dense_matrix' is None
        if int_total_number_of_values_in_a_batch_for_dense_matrix is None:
            int_total_number_of_values_in_a_batch_for_dense_matrix = (
                self.int_total_number_of_values_in_a_batch_for_dense_matrix
            )

        # summarized results of individual component RAMtx for 'combined' RAMtx
        if self.is_combined:
            # %% COMBINED %%
            # (combine result and write summary for the combined RAMtx)
            axis = (
                "features" if self.is_for_querying_features else "barcodes"
            )  # retrieve axis for the current combined RAMtx object (will be always the axis for querying)
            if (
                self._ramdata is None
            ):  # if current combined ramtx is not attached to the ramdata, exit
                return
            if (
                self._get_path_folder_number_of_records_for_each_entry(axis=axis)
                is not None
            ):  # if the output already exists, exit
                return
            if (
                self._path_folder_ramtx_modifiable is None
            ):  # if modifiable RAMtx does not exist, exit
                return
            ax = (
                self._ramdata.ft if self.is_for_querying_features else self._ramdata.bc
            )  # retrieve axis for querying
            len_axis = (
                ax.int_num_entries
            )  # retrieve the length of the axis for querying
            flag_is_interleaved = (
                ax.is_interleaved
            )  # retrieve flag indicating whether the current axis for querying is interleaved.
            int_num_entries_in_a_batch = (
                int_num_chunks_in_a_batch_for_index_of_sparse_matrix * int_size_chunk
            )  # retrieve the number of entries in a batch

            # open zarr objects
            za = ZarrServer(
                f"{self._path_folder_ramtx_modifiable}matrix.{axis}.number_of_records_for_each_entry.zarr/",
                mode="w",
                shape=(len_axis,),
                chunks=(int_size_chunk,),
                dtype=np.float64,
                flag_spawn=flag_spawn,
            )  # open zarr object of the current RAMtx object
            za_bool = ZarrServer(
                f"{self._path_folder_ramtx_modifiable}matrix.{axis}.active_entries.zarr/",
                mode="w",
                shape=(len_axis,),
                chunks=(int_size_chunk,),
                dtype=bool,
                flag_spawn=flag_spawn,
            )  # open zarr object of the current RAMtx object
            if flag_is_interleaved:
                # %% COMBINED - INTERLEAVED %%
                int_pos = 0
                while int_pos < len_axis:
                    # initialize batch
                    st_batch, en_batch = int_pos, min(
                        len_axis, int_pos + int_num_entries_in_a_batch
                    )
                    int_num_entries_batch = (
                        en_batch - st_batch
                    )  # retrieve the number of entries in a batch
                    arr_num_records = np.zeros(int_num_entries_batch, dtype=float)
                    arr_num_active = np.zeros(int_num_entries_batch, dtype=bool)

                    for rtx, dict_index_mapping_from_combined_to_component in zip(
                        self._l_rtx, ax._l_dict_index_mapping_from_combined_to_component
                    ):
                        if rtx is None:  # ignore invalid rtx
                            continue
                        # open zarr objects of the current component RAMtx
                        path_folder = (
                            rtx._get_path_folder_number_of_records_for_each_entry(
                                axis=axis
                            )
                        )
                        assert (
                            path_folder is not None
                        )  # the ramtx object should have the summary result for the current axis
                        za_component = ZarrServer(
                            f"{path_folder}matrix.{axis}.number_of_records_for_each_entry.zarr/",
                            mode="r",
                            flag_spawn=flag_spawn,
                        )
                        za_bool_component = ZarrServer(
                            f"{path_folder}matrix.{axis}.active_entries.zarr/",
                            mode="r",
                            flag_spawn=flag_spawn,
                        )  # open zarr object of the current RAMtx object

                        # retrieve coordinate for the current batch for the current component
                        l_int_entry_combined_batch, l_int_entry_component_batch = (
                            [],
                            [],
                        )  # initialize list of entries for a batch
                        for int_entry_combined in range(st_batch, en_batch):
                            if (
                                int_entry_combined
                                in dict_index_mapping_from_combined_to_component
                            ):
                                l_int_entry_combined_batch.append(int_entry_combined)
                                l_int_entry_component_batch.append(
                                    dict_index_mapping_from_combined_to_component[
                                        int_entry_combined
                                    ]
                                )

                        # update data for the batch
                        if len(l_int_entry_combined_batch) > 0:
                            arr_num_records[
                                l_int_entry_combined_batch
                            ] += za_component.get_coordinate_selection(
                                l_int_entry_component_batch
                            )
                            arr_num_active[
                                l_int_entry_combined_batch
                            ] += za_bool_component.get_coordinate_selection(
                                l_int_entry_component_batch
                            )
                        # terminate spawned processes
                        za_component.terminate()
                        za_bool_component.terminate()
                    # write result for the batch
                    za[st_batch:en_batch] = arr_num_records
                    za_bool[st_batch:en_batch] = arr_num_active
                    int_pos += int_num_entries_in_a_batch  # update 'int_pos'
            else:
                # %% COMBINED - STACKED %%
                int_pos_combined = 0  # initialize
                for (
                    rtx,
                    ax_component,
                    dict_index_mapping_from_combined_to_component,
                ) in zip(
                    self._l_rtx,
                    ax._l_ax,
                    ax._l_dict_index_mapping_from_combined_to_component,
                ):
                    if rtx is not None:  # if rtx is valid
                        int_pos_component = 0  # initialize component iteration
                        # open zarr objects of the current component RAMtx
                        path_folder = (
                            rtx._get_path_folder_number_of_records_for_each_entry(
                                axis=axis
                            )
                        )
                        assert (
                            path_folder is not None
                        )  # the ramtx object should have the summary result for the current axis
                        za_component = ZarrServer(
                            f"{path_folder}matrix.{axis}.number_of_records_for_each_entry.zarr/",
                            mode="r",
                            flag_spawn=flag_spawn,
                        )
                        za_bool_component = ZarrServer(
                            f"{path_folder}matrix.{axis}.active_entries.zarr/",
                            mode="r",
                            flag_spawn=flag_spawn,
                        )  # open zarr object of the current RAMtx object

                        while int_pos_component < ax_component.int_num_entries:
                            st_component, en_component = int_pos_component, min(
                                ax_component.int_num_entries,
                                int_pos_component + int_num_entries_in_a_batch,
                            )
                            int_num_entries_in_a_batch = en_component - st_component

                            # write summary for combined ramtx
                            za[
                                int_pos_combined
                                + st_component : int_pos_combined
                                + en_component
                            ] = za_component[st_component:en_component]
                            za_bool[
                                int_pos_combined
                                + st_component : int_pos_combined
                                + en_component
                            ] = za_bool_component[st_component:en_component]

                            int_pos_component += (
                                int_num_entries_in_a_batch  # update 'int_pos_component'
                            )
                        # terminate spawned processes
                        za_component.terminate()
                        za_bool_component.terminate()
                    int_pos_combined += (
                        ax_component.int_num_entries
                    )  # update 'int_pos_combined'
            # terminate spawned processes
            za.terminate()
            za_bool.terminate()
            return

        """ prepare """
        # if current RAMtx object is located remotely, re-load zarr objects to avoid fork-non-safe runtime error (http/s3 zarr objects appears to be not fork-safe)
        rtx_fork_safe = self.get_fork_safe_version()
        za_mtx_index, za_mtx = rtx_fork_safe.get_za()

        # for each axis
        for axis in axes:
            # check validity of the axis name
            if axis not in {"barcodes", "features"}:
                continue

            flag_axis_is_barcode = axis == "barcodes"
            # skip if result is already available
            flag_res_already_available = False  # initialize
            for path_folder in [
                self._path_folder_ramtx,
                self._path_folder_ramtx_modifiable,
            ]:
                if path_folder is not None and zarr_exists(
                    f"{path_folder}matrix.{axis}.number_of_records_for_each_entry.zarr/",
                    filesystemserver=self.fs,
                ):
                    flag_res_already_available = True
                    break
            if flag_res_already_available:
                continue

            # if no modifiable ramtx object is available, exit
            if self._path_folder_ramtx_modifiable is None:
                continue

            # if the sparse matrix not for querying with the current axis, continue
            if self.is_sparse and axis not in self.mode:
                continue

            # ignore dense ramtx object if 'flag_ignore_dense' is True
            if flag_ignore_dense and not self.is_sparse:
                continue

            # perform survey
            len_axis = (
                self._int_num_barcodes
                if flag_axis_is_barcode
                else self._int_num_features
            )  # retrieve the length of the axis for querying

            # perform survey
            # start worker
            def __write_result(pipe_receiver):
                """# 2022-12-03 17:14:57
                write survey results as zarr objects
                """
                # create a zarr array object that is fork-safe (use ZarrServer if fork-safe zarr object is required, and use typical zarr object in other cases)
                za = ZarrServer(
                    f"{self._path_folder_ramtx_modifiable}matrix.{axis}.number_of_records_for_each_entry.zarr/",
                    mode="w",
                    shape=(len_axis,),
                    chunks=(int_size_chunk,),
                    dtype=np.float64,
                    flag_spawn=self.is_remote,
                )
                za_bool = ZarrServer(
                    f"{self._path_folder_ramtx_modifiable}matrix.{axis}.active_entries.zarr/",
                    mode="w",
                    shape=(len_axis,),
                    chunks=(int_size_chunk,),
                    dtype=bool,
                    flag_spawn=self.is_remote,
                )

                while True:
                    l_r = pipe_receiver.recv()
                    if l_r is None:
                        break
                    int_num_entries = sum(
                        len(r[1]) for r in l_r
                    )  # retrieve the total number of entries in the 'l_r'
                    pos = 0  # initialize
                    arr_coord_combined, arr_num_records_combined = np.zeros(
                        int_num_entries, dtype=np.int64
                    ), np.zeros(int_num_entries, dtype=np.int64)
                    for r in l_r:
                        sl, arr_num_records = r  # parse r
                        int_num_entries_in_r = len(arr_num_records)
                        arr_coord_combined[
                            pos : pos + int_num_entries_in_r
                        ] = np.arange(
                            sl.start, sl.stop
                        )  # update 'arr_coord_combined'
                        arr_num_records_combined[
                            pos : pos + int_num_entries_in_r
                        ] = arr_num_records  # update 'arr_coord_combined'
                        pos += int_num_entries_in_r  # update 'pos'
                    del l_r, r

                    za.set_coordinate_selection(
                        (arr_coord_combined,), arr_num_records_combined
                    )  # save the number of records
                    za_bool.set_coordinate_selection(
                        (arr_coord_combined,), arr_num_records_combined > 0
                    )  # active entry is defined by finding entries with at least one count record
                    del arr_coord_combined, arr_num_records_combined

                # terminate the zarr servers
                za.terminate()
                za_bool.terminate()

            pipe_sender, pipe_receiver = mp.Pipe()
            p = mp.Process(target=__write_result, args=(pipe_receiver,))
            p.start()
            ns = {
                "pipe_sender": pipe_sender,
                "l_buffer": [],
                "int_size_buffer": 20,
            }  # a namespace that will be shared between different scopes

            if self.is_sparse:  # survey for sparse matrix
                """%% Sparse matrix %%"""
                # surveying on the axis of the sparse matrix
                int_num_entries_processed = 0
                int_num_entries_to_retrieve = int(
                    za_mtx_index.chunks[0]
                    * int_num_chunks_in_a_batch_for_index_of_sparse_matrix
                )
                while int_num_entries_processed < len_axis:
                    sl = slice(
                        int_num_entries_processed,
                        min(
                            len_axis,
                            int_num_entries_processed + int_num_entries_to_retrieve,
                        ),
                    )
                    arr_num_records = (
                        za_mtx_index[sl][:, 1] - za_mtx_index[sl][:, 0]
                    )  # retrieve the number of records
                    int_num_entries_processed += (
                        int_num_entries_to_retrieve  # update the position
                    )
                    # flush buffer
                    ns["l_buffer"].append((sl, arr_num_records))
                    if len(ns["l_buffer"]) >= ns["int_size_buffer"]:
                        ns["pipe_sender"].send(ns["l_buffer"])  # send result to worker
                        ns["l_buffer"] = []  # initialize the buffer
                    del arr_num_records
            else:  # survey for dense matrix (multi-processed)
                """%% Dense matrix %%"""
                # prepare
                len_axis_secondary = (
                    self._int_num_features
                    if flag_axis_is_barcode
                    else self._int_num_barcodes
                )  # retrieve the length of the axis not for querying

                # retrieve chunk size for each axis
                (
                    int_size_chunk_axis_for_querying,
                    int_size_chunk_axis_not_for_querying,
                ) = (
                    za_mtx.chunks[0 if flag_axis_is_barcode else 1],
                    za_mtx.chunks[1 if flag_axis_is_barcode else 0],
                )

                # retrieve entries for each axis for batch and a subbatch
                int_num_entries_in_a_batch_in_axis_for_querying = (
                    int_size_chunk_axis_for_querying
                    * int_num_chunks_in_a_batch_for_axis_for_querying_dense
                )
                int_num_entries_in_a_subbatch_in_axis_not_for_querying = max(
                    1,
                    int(
                        np.floor(
                            int_total_number_of_values_in_a_batch_for_dense_matrix
                            / int_num_entries_in_a_batch_in_axis_for_querying
                        )
                    ),
                )

                def __gen_batch():
                    """# 2022-08-15 20:16:51
                    generate batch on the primary axis
                    """
                    # initialize looping through axis for querying (primary axis)
                    int_num_entries_processed_in_axis_for_querying = 0
                    while int_num_entries_processed_in_axis_for_querying < len_axis:
                        sl = slice(
                            int_num_entries_processed_in_axis_for_querying,
                            min(
                                len_axis,
                                int_num_entries_processed_in_axis_for_querying
                                + int_num_entries_in_a_batch_in_axis_for_querying,
                            ),
                        )  # retrieve a slice along the primary axis
                        yield {
                            "sl": sl,
                            "int_num_entries_processed_in_axis_for_querying": int_num_entries_processed_in_axis_for_querying,
                        }
                        int_num_entries_processed_in_axis_for_querying += int_num_entries_in_a_batch_in_axis_for_querying  # update the position

                def __process_batch(pipe_receiver_batch, pipe_sender_result):
                    """# 2022-09-06 17:15:42
                    process batches containing entries on the primary axis
                    """
                    while True:
                        batch = pipe_receiver_batch.recv()
                        if batch is None:
                            break
                        # parse batch
                        sl, int_num_entries_processed_in_axis_for_querying = (
                            batch["sl"],
                            batch["int_num_entries_processed_in_axis_for_querying"],
                        )

                        # initialize looping through axis not for querying (secondary axis)
                        int_num_entries_processed_in_axis_not_for_querying = 0
                        arr_num_records = np.zeros(
                            sl.stop - sl.start, dtype=np.int64
                        )  # initialize the list of the number of records for the entries in the current batch
                        while (
                            int_num_entries_processed_in_axis_not_for_querying
                            < len_axis_secondary
                        ):
                            sl_secondary = slice(
                                int_num_entries_processed_in_axis_not_for_querying,
                                min(
                                    len_axis_secondary,
                                    int_num_entries_processed_in_axis_not_for_querying
                                    + int_num_entries_in_a_subbatch_in_axis_not_for_querying,
                                ),
                            )  # retrieve a slice along the secondary axis
                            arr_num_records += (
                                (
                                    za_mtx.get_orthogonal_selection(
                                        (sl, sl_secondary)
                                    ).T
                                    if flag_axis_is_barcode
                                    else za_mtx.get_orthogonal_selection(
                                        (sl_secondary, sl)
                                    )
                                )
                                > 0
                            ).sum(
                                axis=0
                            )  # update 'arr_num_records'
                            int_num_entries_processed_in_axis_not_for_querying += int_num_entries_in_a_subbatch_in_axis_not_for_querying  # update the position
                        # send the result
                        pipe_sender_result.send((sl, arr_num_records))

                def __post_process_batch(res):
                    """# 2022-08-15 21:03:59
                    process result from a batch
                    """
                    sl, arr_num_records = res  # parse the result
                    # flush buffer
                    ns["l_buffer"].append((sl, arr_num_records))
                    if len(ns["l_buffer"]) >= ns["int_size_buffer"]:
                        ns["pipe_sender"].send(ns["l_buffer"])  # send result to worker
                        ns["l_buffer"] = []  # initialize the buffer

                # process batch by batch
                bk.Multiprocessing_Batch_Generator_and_Workers(
                    gen_batch=__gen_batch(),
                    process_batch=__process_batch,
                    post_process_batch=__post_process_batch,
                    int_num_threads=int_num_threads,
                )

            # flush the buffer
            if len(ns["l_buffer"]) > 0:
                pipe_sender.send(ns["l_buffer"])  # send result to worker
            # dismiss the worker
            pipe_sender.send(None)
            p.join()

        # destroy zarr server
        rtx_fork_safe.terminate_spawned_processes()

    """ <Methods for Synchronization> """

    @property
    def use_locking(self):
        """# 2022-12-12 02:45:43
        return True if a spin lock algorithm is being used for synchronization of operations on the current object
        """
        return self._zsls is not None

    def _save_metadata_(self):
        """# 2022-07-31 00:40:33
        a method for saving metadata to the disk
        """
        if (
            not self._flag_is_read_only and not self.is_combined
        ):  # update metadata only when the current RamData object is not read-only # do not update metadata when current RAMtx is in combined mode
            if hasattr(self, "_dict_metadata"):  # if metadata has been loaded
                if self.use_locking:  # %% FILE LOCKING %%
                    self._zsls.acquire_lock(f"{self._path_folder_ramtx}.zattrs.lock")
                self._root.attrs[
                    "dict_metadata"
                ] = self._dict_metadata  # update metadata
                if self.use_locking:  # %% FILE LOCKING %%
                    self._zsls.release_lock(f"{self._path_folder_ramtx}.zattrs.lock")

    """ </Methods for Synchronization> """

    @property
    def n_active_entries(self):
        """# 2022-08-30 13:45:34
        calculate the number of active entries
        """
        if self.is_combined:
            # %% COMBINED %%
            return sum(
                rtx.n_active_entries for rtx in self._l_rtx
            )  # return the number of active entries of the combined ramtx object
        else:
            # calculate the number of active entries if it has not been calculated.
            if not "n_active_entries" in self._dict_metadata:
                self.ba_active_entries
            return (
                self._dict_metadata["n_active_entries"]
                if "n_active_entries" in self._dict_metadata
                else self.len_axis_for_querying
            )  # if the number of active entries cannot be calculated, return the number of all entries

    def __repr__(self):
        return f"<RAMtx object ({self.mode}) for querying '{'features' if self.is_for_querying_features else  'barcodes'}' containing {self._int_num_records} records of {self._int_num_features} features X {self._int_num_barcodes} barcodes\n\tRAMtx path: {self._path_folder_ramtx}>"

    @property
    def ba_filter_features(self):
        """# 2022-06-23 17:05:55
        returns 'ba_filter'
        """
        return self._ba_filter_features

    @ba_filter_features.setter
    def ba_filter_features(self, ba_filter):
        """# 2022-06-23 17:06:36
        check whether the filter is valid
        """
        if ba_filter is not None:
            assert len(ba_filter) == self._int_num_features
        self._ba_filter_features = ba_filter

    @property
    def ba_filter_barcodes(self):
        """# 2022-06-23 17:18:56
        returns 'ba_filter'
        """
        return self._ba_filter_barcodes

    @ba_filter_barcodes.setter
    def ba_filter_barcodes(self, ba_filter):
        """# 2022-06-23 17:19:00
        check whether the filter is valid
        """
        if ba_filter is not None:
            assert len(ba_filter) == self._int_num_barcodes
        self._ba_filter_barcodes = ba_filter

    @property
    def is_for_querying_features(self):
        """# 2022-07-30 20:37:02"""
        return self._is_for_querying_features

    @is_for_querying_features.setter
    def is_for_querying_features(self, flag):
        """# 2022-07-30 20:37:37"""
        if self.is_combined:
            # %% COMBINED %%
            for rtx in self._l_rtx:  # set the flag for individual component RAMtx
                if rtx is not None:
                    rtx.is_for_querying_features = flag
            return

        if (
            self.is_sparse
        ):  # if current RAMtx is in sparse format, this property is fixed
            return
        self._is_for_querying_features = flag  # update property

    @property
    def flag_ramtx_sorted_by_id_feature(self):
        """# 2022-06-23 09:06:51
        retrieve 'flag_ramtx_sorted_by_id_feature' setting from the RAMtx metadata
        """
        return (
            self._dict_metadata["flag_ramtx_sorted_by_id_feature"]
            if self.is_sparse
            else None
        )

    @property
    def len_axis_for_querying(self):
        """# 2022-06-23 09:08:44
        retrieve number of elements of the indexed axis
        """
        return (
            self._int_num_features
            if self.is_for_querying_features
            else self._int_num_barcodes
        )

    @property
    def len_axis_not_for_querying(self):
        """# 2022-06-23 09:08:44
        retrieve number of elements of the not indexed axis
        """
        return (
            self._int_num_barcodes
            if self.is_for_querying_features
            else self._int_num_features
        )

    @property
    def axis_for_querying(self):
        """
        # 2022-06-30 21:45:48
        return 'Axis' object of the indexed axis
        """
        return (
            None
            if self._ramdata is None
            else (
                self._ramdata.ft if self.is_for_querying_features else self._ramdata.bc
            )
        )

    @property
    def ba_filter_axis_for_querying(self):
        """# 2022-06-23 09:08:44
        retrieve filter of the indexed axis
        """
        return (
            self.ba_filter_features
            if self.is_for_querying_features
            else self.ba_filter_barcodes
        )

    def __contains__(self, x) -> bool:
        """# 2022-06-23 09:13:31
        check whether an integer representation of indexed entry is available in the index. if filter is active, also check whether the entry is active
        """
        return (0 <= x < self.len_axis_for_querying) and (
            self.ba_filter_axis_for_querying is None
            or self.ba_filter_axis_for_querying[x]
        )  # x should be in valid range, and if it is, check whether x is an active element in the filter (if filter has been set)

    def __iter__(self):
        """# 2022-06-23 09:13:46
        yield each entry in the index upon iteration. if filter is active, ignore inactive elements
        """
        if (
            self.ba_filter_axis_for_querying is None
        ):  # if filter is not set, iterate over all elements
            return iter(range(self.len_axis_for_querying))
        else:  # if filter is active, yield indices of active elements only
            return iter(BA.to_integer_indices(self.ba_filter_axis_for_querying))

    def drop_reference(self):
        """# 2022-10-20 00:11:09
        for a combined RAMtx object, drop a RAMtx object from the reference RamData
        """
        if not hasattr(self, "_reference_dropped"):
            if self.is_combined:  # for combined RAMtx
                ram = self._ramdata  # retrieve associated RamData
                if ram is not None:  # if ramdata exists
                    if (
                        ram.is_combined
                        and ram.int_index_component_reference is not None
                    ):  # if reference component is active
                        self._l_rtx[
                            ram.int_index_component_reference
                        ] = None  # set the rtx object of the reference to None (ignore the data of reference)
            self._reference_dropped = (
                True  # set the attribute indicating the reference has been dropped
            )

    def __getitem__(self, l_int_entry):
        """# 2022-09-20 18:13:41
        Retrieve data of a given list of entries from RAMtx as lists of values and arrays (i.e. sparse matrix), each value and array contains data of a single 'int_entry' of the indexed axis
        '__getitem__' can be used to retrieve minimal number of values required to build a sparse matrix or dense matrix from it

        Returns:
        l_int_entry_of_axis_for_querying, l_arr_intinfor_entry_of_axis_not_for_querying, l_arr_value :
            'l_int_entry_of_axis_for_querying' only contains int_entry of valid entries
        """
        """ prepare """
        # if current RAMtx object is located remotely, re-load zarr objects to avoid fork-non-safe runtime error (http zarr objects appears to be not fork-safe)
        za_mtx_index, za_mtx = self.get_za()

        # drop the RAMtx object of the reference
        self.drop_reference()

        # retrieve settings
        int_total_number_of_values_in_a_batch_for_dense_matrix = (
            self.int_total_number_of_values_in_a_batch_for_dense_matrix
        )

        # initialize the output data structures
        (
            l_int_entry_of_axis_for_querying,
            l_arr_int_entry_of_axis_not_for_querying,
            l_arr_value,
        ) = ([], [], [])

        # wrap in a list if a single entry was queried
        if isinstance(
            l_int_entry, (int, np.int64, np.int32, np.int16, np.int8)
        ):  # check whether the given entry is an integer
            l_int_entry = [l_int_entry]

        flag_empty_input = len(l_int_entry) == 0  # retrieve flag indicating empty input
        # logger.info( f'flag_empty_input: {flag_empty_input}' )

        # %% COMBINED %%
        # translate query entries of the combined ramtx to the entries of a component ramtx
        dict_index_mapping_from_combined_to_component_axis_for_querying = (
            self._dict_index_mapping_from_combined_to_component_ft
            if self.is_for_querying_features
            else self._dict_index_mapping_from_combined_to_component_bc
        )
        if dict_index_mapping_from_combined_to_component_axis_for_querying is not None:
            l_int_entry = list(
                dict_index_mapping_from_combined_to_component_axis_for_querying[
                    int(int_entry)
                ]
                for int_entry in l_int_entry
                if int_entry
                in dict_index_mapping_from_combined_to_component_axis_for_querying
            )

        """ retrieve filters """
        is_for_querying_features = self.is_for_querying_features
        ba_filter_axis_for_querying, ba_filter_not_axis_for_querying = (
            (self.ba_filter_features, self.ba_filter_barcodes)
            if is_for_querying_features
            else (self.ba_filter_barcodes, self.ba_filter_features)
        )

        """ filter 'int_entry', if a filter has been set """
        """ handle when empty 'l_int_entry' has been given and filter has been set  """
        # logger.info( f'ba_filter_axis_for_querying: {len(ba_filter_axis_for_querying) if ba_filter_axis_for_querying is not None else None}' )
        if ba_filter_axis_for_querying is not None:
            l_int_entry = (
                BA.to_integer_indices(ba_filter_axis_for_querying)
                if flag_empty_input
                else list(
                    int_entry
                    for int_entry in l_int_entry
                    if ba_filter_axis_for_querying[int_entry]
                )
            )  # filter 'l_int_entry' or use the entries in the given filter (if no int_entry was given, use all active entries in the filter)
        # logger.info( f'l_int_entry: {len(l_int_entry)}' )

        # if no valid entries are available, return an empty result
        if len(l_int_entry) == 0:
            return (
                l_int_entry_of_axis_for_querying,
                l_arr_int_entry_of_axis_not_for_querying,
                l_arr_value,
            )

        """ sort 'int_entry' so that closely located entries can be retrieved together """
        # sort indices of entries so that the data access can occur in the same direction across threads
        int_num_entries = len(l_int_entry)
        if (
            int_num_entries > 30
        ):  # use numpy sort function only when there are sufficiently large number of indices of entries to be sorted
            l_int_entry = np.sort(l_int_entry)
        else:
            l_int_entry = sorted(l_int_entry)

        """
        retrieve data from the Combined RAMtx data structure
        """
        # handle combined ramtx
        if self.is_combined:
            # %% COMBINED %%
            # collect data from each component
            dict_data = dict()
            for rtx in self._l_rtx:
                if rtx is not None:
                    for (
                        int_entry,
                        arr_int_entry_of_axis_not_for_querying,
                        arr_value,
                    ) in zip(
                        *rtx[l_int_entry]
                    ):  # retrieve data from the component
                        # collect retrieved data
                        if int_entry not in dict_data:
                            dict_data[int_entry] = {
                                "l_arr_int_entry_of_axis_not_for_querying": [],
                                "l_arr_value": [],
                            }  # initialize
                        dict_data[int_entry][
                            "l_arr_int_entry_of_axis_not_for_querying"
                        ].append(arr_int_entry_of_axis_not_for_querying)
                        dict_data[int_entry]["l_arr_value"].append(arr_value)

            # combine data for each entry
            for int_entry in sorted(dict_data):  # sort 'int_entry'
                l_int_entry_of_axis_for_querying.append(int_entry)
                l_arr_int_entry_of_axis_not_for_querying.append(
                    np.concatenate(
                        dict_data[int_entry]["l_arr_int_entry_of_axis_not_for_querying"]
                    )
                )
                l_arr_value.append(np.concatenate(dict_data[int_entry]["l_arr_value"]))
            return (
                l_int_entry_of_axis_for_querying,
                l_arr_int_entry_of_axis_not_for_querying,
                l_arr_value,
            )

        """
        retrieve data from the RAMtx data structure (self.is_combined should be False)
        """
        # retrieve flags for dtype conversions
        flag_change_dtype_of_values = za_mtx.dtype != self._dtype_of_values

        """ create view """
        # retrieve dictionaries for changing coordinates
        (
            dict_change_int_entry_of_axis_for_querying,
            dict_change_int_entry_of_axis_not_for_querying,
        ) = (
            None,
            None,
        )  # initialize the dictionaries
        if (
            self._ramdata is not None
        ):  # if RAMtx has been attached to RamData, retrieve dictionaries that can be used to change coordinate
            ram = (
                self._ramdata._ramdata_composite if self.is_component else self._ramdata
            )  # retrieve ramdata from which view will be retrieved. if current RAMtx is component, use view of the composite RamData. Else, use RamData to which current RAMtx has been attached to.
            if self.is_for_querying_features:
                dict_change_int_entry_of_axis_for_querying = ram.ft.dict_change
                dict_change_int_entry_of_axis_not_for_querying = ram.bc.dict_change
            else:
                dict_change_int_entry_of_axis_for_querying = ram.bc.dict_change
                dict_change_int_entry_of_axis_not_for_querying = ram.ft.dict_change

        # compose a vectorized function for the conversion of int_entries of the non-indexed axis.
        def f(i):
            return dict_change_int_entry_of_axis_not_for_querying[i]

        vchange_int_entry_of_axis_not_for_querying = (
            np.vectorize(f)
            if dict_change_int_entry_of_axis_not_for_querying is not None
            else None
        )

        """ create combined axis """
        # retrieve dictionaries for changing coordinates for mapping components to combined data
        (
            dict_change_int_entry_component_of_axis_for_querying,
            dict_change_int_entry_component_of_axis_not_for_querying,
        ) = (
            None,
            None,
        )  # initialize the dictionaries
        if self.is_component:  # if RAMtx is component of combined RAMtx
            if self.is_for_querying_features:
                dict_change_int_entry_component_of_axis_for_querying = (
                    self._dict_index_mapping_from_component_to_combined_ft
                )
                dict_change_int_entry_component_of_axis_not_for_querying = (
                    self._dict_index_mapping_from_component_to_combined_bc
                )
            else:
                dict_change_int_entry_component_of_axis_for_querying = (
                    self._dict_index_mapping_from_component_to_combined_bc
                )
                dict_change_int_entry_component_of_axis_not_for_querying = (
                    self._dict_index_mapping_from_component_to_combined_ft
                )

        # compose a vectorized function for the conversion of int_entry_component of the non-indexed axis.
        def f_component(i):
            return dict_change_int_entry_component_of_axis_not_for_querying[i]

        vchange_int_entry_component_of_axis_not_for_querying = (
            np.vectorize(f_component)
            if dict_change_int_entry_component_of_axis_not_for_querying is not None
            else None
        )

        """ change component """
        # retrieve dictionaries for changing coordinates for changing components on a combined axis
        (
            dict_change_int_entry_combined_axis_for_querying,
            dict_change_int_entry_combined_axis_not_for_querying,
        ) = (
            None,
            None,
        )  # initialize the dictionaries
        if self.is_component:  # if RAMtx is component of combined RAMtx
            ram = (
                self._ramdata._ramdata_composite if self.is_component else self._ramdata
            )  # retrieve ramdata from which view will be retrieved. if current RAMtx is component, use composite RamData. else, use RamData to which current RAMtx has been attached to.
            if self.is_for_querying_features:
                dict_change_int_entry_combined_axis_for_querying = (
                    ram.ft._dict_index_mapping_from_combined_to_dest_component
                )
                dict_change_int_entry_combined_axis_not_for_querying = (
                    ram.bc._dict_index_mapping_from_combined_to_dest_component
                )
            else:
                dict_change_int_entry_combined_axis_for_querying = (
                    ram.bc._dict_index_mapping_from_combined_to_dest_component
                )
                dict_change_int_entry_combined_axis_not_for_querying = (
                    ram.ft._dict_index_mapping_from_combined_to_dest_component
                )

        # compose a vectorized function for the conversion of int_entry_component of the non-indexed axis.
        def f_combined(i):
            return dict_change_int_entry_combined_axis_not_for_querying[i]

        vchange_int_entry_combined_axis_not_for_querying = (
            np.vectorize(f_combined)
            if dict_change_int_entry_combined_axis_not_for_querying is not None
            else None
        )

        """ internal settings """
        int_num_chunks_for_a_batch = (
            2  # number of chunks in a batch for retrieving data for the sparse matrix
        )

        def __retrieve_data(
            pipe_from_main_thread=None, pipe_to_main_thread=None, flag_as_a_worker=True
        ):
            """# 2022-08-16 01:54:31
            retrieve data as a worker in a worker process or in the main processs (in single-process mode)
            """
            # if current RAMtx object is located remotely, re-load zarr objects to avoid fork-non-safe runtime error (http/s3 zarr objects appears to be not fork-safe)
            rtx_fork_safe = self.get_fork_safe_version()
            za_mtx_index, za_mtx = rtx_fork_safe.get_za()

            """ initialize """
            # handle inputs
            l_int_entry = (
                pipe_from_main_thread.recv()
                if flag_as_a_worker
                else pipe_from_main_thread
            )  # receive work if 'flag_as_a_worker' is True or use 'pipe_from_main_thread' as a list of works
            # for each int_entry, retrieve data and collect records
            (
                l_int_entry_of_axis_for_querying,
                l_arr_int_entry_of_axis_not_for_querying,
                l_arr_value,
            ) = ([], [], [])

            def __process_entry(
                int_entry, arr_int_entry_of_axis_not_for_querying, arr_value
            ):
                """# 2022-07-30 22:07:46
                process retrieve data. apply filter and change coordinates
                """
                """ convert dtypes of retrieved data """
                if (
                    flag_change_dtype_of_feature_and_barcode_indices
                ):  # convert to integer type
                    arr_int_entry_of_axis_not_for_querying = (
                        arr_int_entry_of_axis_not_for_querying.astype(
                            self._dtype_of_feature_and_barcode_indices
                        )
                    )
                if flag_change_dtype_of_values:
                    arr_value = arr_value.astype(self._dtype_of_values)

                """ if a filter for not-indexed axis has been set, apply the filter to the retrieved records """
                if ba_filter_not_axis_for_querying is not None:
                    arr_mask = np.zeros(
                        len(arr_int_entry_of_axis_not_for_querying), dtype=bool
                    )  # initialize the mask for filtering records
                    for i, int_entry_of_axis_not_for_querying in enumerate(
                        arr_int_entry_of_axis_not_for_querying
                    ):  # iterate through each record
                        if ba_filter_not_axis_for_querying[
                            int_entry_of_axis_not_for_querying
                        ]:  # check whether the current int_entry is included in the filter
                            arr_mask[i] = True  # include the record
                    # if no valid data exists (all data were filtered out), continue to the next 'int_entry'
                    if arr_mask.sum() == 0:
                        return

                    # filter records using the mask
                    arr_int_entry_of_axis_not_for_querying = (
                        arr_int_entry_of_axis_not_for_querying[arr_mask]
                    )
                    arr_value = arr_value[arr_mask]

                """ # 2022-12-03 19:59:48 
                coordinate conversion process
                
                local coordinates of the current component
                    > global coordinates (on a combined axis) of the current component
                    > global coordinates (on a combined axis) of the destination component (usually reference component)
                    > apply view of the global coordinates (on a combined axis)
                """

                # component > combined axis
                if dict_change_int_entry_component_of_axis_for_querying is not None:
                    int_entry = dict_change_int_entry_component_of_axis_for_querying[
                        int_entry
                    ]
                # convert int_entry_component to int_entry for the non-indexed axis if a mapping has been given (create combined)
                if vchange_int_entry_component_of_axis_not_for_querying is not None:
                    arr_int_entry_of_axis_not_for_querying = (
                        vchange_int_entry_component_of_axis_not_for_querying(
                            arr_int_entry_of_axis_not_for_querying
                        )
                    )

                # combined > component axis
                if dict_change_int_entry_combined_axis_for_querying is not None:
                    if (
                        int_entry
                        not in dict_change_int_entry_combined_axis_for_querying
                    ):  # exclude entry that are absent in the destination component
                        return
                    int_entry = dict_change_int_entry_combined_axis_for_querying[
                        int_entry
                    ]
                # convert int_entry_combined to int_entry for the non-indexed axis if a mapping has been given (change component)
                if vchange_int_entry_combined_axis_not_for_querying is not None:
                    # exclude records that are absent in the destination component
                    arr_mask = np.zeros(
                        len(arr_int_entry_of_axis_not_for_querying), dtype=bool
                    )  # initialize the mask for filtering records
                    for i, int_entry_of_axis_not_for_querying in enumerate(
                        arr_int_entry_of_axis_not_for_querying
                    ):  # iterate through each record
                        if (
                            int_entry_of_axis_not_for_querying
                            in dict_change_int_entry_combined_axis_not_for_querying
                        ):  # check whether the current int_entry is included in the target component
                            arr_mask[i] = True  # include the record
                    # if no valid data exists (all data were filtered out), continue to the next 'int_entry'
                    if arr_mask.sum() == 0:
                        return

                    # filter records using the mask
                    arr_int_entry_of_axis_not_for_querying = (
                        arr_int_entry_of_axis_not_for_querying[arr_mask]
                    )
                    arr_value = arr_value[arr_mask]

                    # change coordinates
                    arr_int_entry_of_axis_not_for_querying = (
                        vchange_int_entry_combined_axis_not_for_querying(
                            arr_int_entry_of_axis_not_for_querying
                        )
                    )

                # apply view
                if dict_change_int_entry_of_axis_for_querying is not None:
                    int_entry = dict_change_int_entry_of_axis_for_querying[int_entry]
                # convert int_entry for the non-indexed axis if a mapping has been given (create view)
                if vchange_int_entry_of_axis_not_for_querying is not None:
                    arr_int_entry_of_axis_not_for_querying = (
                        vchange_int_entry_of_axis_not_for_querying(
                            arr_int_entry_of_axis_not_for_querying
                        )
                    )

                """ append the retrieved data to the output results """
                l_int_entry_of_axis_for_querying.append(
                    int_entry
                )  # convert int_entry for the indexed axis if a mapping has been given
                l_arr_int_entry_of_axis_not_for_querying.append(
                    arr_int_entry_of_axis_not_for_querying
                )
                l_arr_value.append(arr_value)

            def __fetch_from_sparse_ramtx(l_int_entry_in_a_batch, l_index_in_a_batch):
                """# 2022-07-30 22:32:14
                fetch data from sparse ramtx for a batch
                """
                arr_index_of_a_batch = np.array(
                    l_index_in_a_batch
                )  # convert index of the batch to a numpy array
                st_batch, en_batch = (
                    arr_index_of_a_batch[0, 0],
                    arr_index_of_a_batch[-1, 1],
                )  # retrieve start and end positions of the current batch
                (
                    arr_int_entry_of_axis_not_for_querying,
                    arr_value,
                ) = za_mtx.get_orthogonal_selection(
                    slice(st_batch, en_batch)
                ).T  # fetch data from the Zarr object

                for int_entry, index in zip(
                    l_int_entry_in_a_batch, arr_index_of_a_batch - st_batch
                ):  # substract the start position of the batch to retrieve the local index
                    st, en = index
                    sl = slice(st, en)
                    __process_entry(
                        int_entry,
                        arr_int_entry_of_axis_not_for_querying[sl],
                        arr_value[sl],
                    )

            def __fetch_from_dense_ramtx(l_int_entry_in_a_batch):
                """# 2022-08-16 01:54:21
                fetch data from dense ramtx for a batch in a memory-efficient manner using subbatches
                """
                # initialize the sparse data container for each entry
                dict_data = dict()

                # retrieve entries for a subbatch
                int_num_entries_in_a_subbatch_in_axis_not_for_querying = max(
                    1,
                    int(
                        np.floor(
                            int_total_number_of_values_in_a_batch_for_dense_matrix
                            / len(l_int_entry_in_a_batch)
                        )
                    ),
                )  # minimum number of entries in a subbatch is 1

                # initialize looping through axis not for querying (secondary axis)
                int_num_entries_processed_in_axis_not_for_querying = 0
                while (
                    int_num_entries_processed_in_axis_not_for_querying
                    < self.len_axis_not_for_querying
                ):  # iterate through each subbatch
                    sl_secondary = slice(
                        int_num_entries_processed_in_axis_not_for_querying,
                        min(
                            self.len_axis_not_for_querying,
                            int_num_entries_processed_in_axis_not_for_querying
                            + int_num_entries_in_a_subbatch_in_axis_not_for_querying,
                        ),
                    )  # retrieve a slice along the secondary axis

                    # iterate through each entry on the axis for querying for the current subbatch
                    for int_entry, arr_data in zip(
                        l_int_entry_in_a_batch,
                        za_mtx.get_orthogonal_selection(
                            (sl_secondary, l_int_entry_in_a_batch)
                        ).T
                        if is_for_querying_features
                        else za_mtx.get_orthogonal_selection(
                            (l_int_entry_in_a_batch, sl_secondary)
                        ),
                    ):  # fetch data from the Zarr object for the current subbatch and iterate through each entry and its data
                        arr_int_entry_of_axis_not_for_querying = np.where(arr_data)[
                            0
                        ]  # retrieve coordinates of non-zero records
                        if (
                            len(arr_int_entry_of_axis_not_for_querying) == 0
                        ):  # if no non-zero records exist, continue to the next entry
                            continue
                        arr_value = arr_data[
                            arr_int_entry_of_axis_not_for_querying
                        ]  # retrieve non-zero records
                        arr_int_entry_of_axis_not_for_querying += int_num_entries_processed_in_axis_not_for_querying  # add offset 'int_num_entries_processed_in_axis_not_for_querying' to the coordinates retrieved from the subbatch
                        del arr_data

                        # initialize 'int_entry' for the sparse data container
                        if int_entry not in dict_data:
                            dict_data[int_entry] = {
                                "l_arr_int_entry_of_axis_not_for_querying": [],
                                "l_arr_value": [],
                            }
                        # add retrieved data from the subbatch to the sparse data container
                        dict_data[int_entry][
                            "l_arr_int_entry_of_axis_not_for_querying"
                        ].append(arr_int_entry_of_axis_not_for_querying)
                        dict_data[int_entry]["l_arr_value"].append(arr_value)
                        del arr_value, arr_int_entry_of_axis_not_for_querying

                    int_num_entries_processed_in_axis_not_for_querying += int_num_entries_in_a_subbatch_in_axis_not_for_querying  # update the position

                for int_entry in dict_data:  # iterate each entry
                    __process_entry(
                        int_entry,
                        np.concatenate(
                            dict_data[int_entry][
                                "l_arr_int_entry_of_axis_not_for_querying"
                            ]
                        ),
                        np.concatenate(dict_data[int_entry]["l_arr_value"]),
                    )  # concatenate list of arrays into a single array
                del dict_data

            #                 logger.info( f"ramtx getitem __fetch_from_dense_ramtx completed for {len( l_int_entry_in_a_batch )} entries" )

            """ retrieve data """
            if self.is_sparse:  # handle sparse ramtx
                """%% Sparse ramtx %%"""
                # prepare
                int_num_records_in_a_chunk = za_mtx.chunks[
                    0
                ]  # retrieve the number of records in a chunk
                # retrieve flags for dtype conversions
                flag_change_dtype_mtx_index = za_mtx_index.dtype != np.int64
                flag_change_dtype_of_feature_and_barcode_indices = (
                    za_mtx.dtype != self._dtype_of_feature_and_barcode_indices
                )

                # retrieve mtx_index data and remove invalid entries
                arr_index = za_mtx_index.get_orthogonal_selection(
                    l_int_entry
                )  # retrieve mtx_index data
                if (
                    flag_change_dtype_mtx_index
                ):  # convert dtype of retrieved mtx_index data
                    arr_index = arr_index.astype(np.int64)

                index_chunk_start_current_batch = (
                    None  # initialize the index of the chunk at the start of the batch
                )
                l_int_entry_in_a_batch, l_index_in_a_batch = (
                    [],
                    [],
                )  # several entries will be processed together as a batch if they reside in the same or nearby chunk ('int_num_chunks_for_a_batch' setting)
                # iterate through each 'int_entry'
                for int_entry, index in zip(
                    l_int_entry, arr_index
                ):  # iterate through each entry
                    st, en = index
                    if (
                        st == en
                    ):  # if there is no count data for the 'int_entry', continue on to the next 'int_entry' # drop 'int_entry' lacking count data (when start and end index is the same, the 'int_entry' does not contain any data)
                        continue

                    """ if batch is full, flush the batch """
                    index_chunk_end = (
                        en - 1 // int_num_records_in_a_chunk
                    )  # retrieve the index of the last chunk
                    if (
                        index_chunk_start_current_batch is not None
                        and index_chunk_end
                        >= index_chunk_start_current_batch + int_num_chunks_for_a_batch
                    ):  # if start has been set
                        __fetch_from_sparse_ramtx(
                            l_int_entry_in_a_batch, l_index_in_a_batch
                        )
                        l_int_entry_in_a_batch, l_index_in_a_batch = (
                            [],
                            [],
                        )  # initialize the next batch
                        index_chunk_start_current_batch = None  # reset start

                    """ start the batch """
                    # if start has not been set, set the start of the current batch
                    if index_chunk_start_current_batch is None:  # start the batch
                        index_chunk_start_current_batch = (
                            st // int_num_records_in_a_chunk
                        )

                    # add int_entry to the batch
                    l_int_entry_in_a_batch.append(int_entry)
                    l_index_in_a_batch.append([st, en])

                if (
                    len(l_int_entry_in_a_batch) > 0
                ):  # if some entries remains unprocessed, flush the buffer
                    __fetch_from_sparse_ramtx(
                        l_int_entry_in_a_batch, l_index_in_a_batch
                    )
            else:
                """%% Dense ramtx %%"""
                # prepare
                int_num_entries_in_a_chunk = (
                    za_mtx.chunks[1] if is_for_querying_features else za_mtx.chunks[0]
                )  # retrieve the number of entries in a chunk
                flag_change_dtype_of_feature_and_barcode_indices = False  # since indices from dense ramtx (return values of np.where) will be in np.int64 format, there will be no need to change dtype of indices

                index_chunk_start_current_batch = (
                    None  # initialize the index of the chunk at the start of the batch
                )
                l_int_entry_in_a_batch = (
                    []
                )  # several entries will be processed together as a batch if they reside in the same or nearby chunk ('int_num_chunks_for_a_batch' setting)
                # iterate through each 'int_entry'
                #                 logger.info( f"ramtx getitem {len(l_int_entry)} entries will be retrieved" )
                for int_entry in l_int_entry:  # iterate through each entry
                    """if batch is full, flush the batch"""
                    index_chunk = (
                        int_entry // int_num_entries_in_a_chunk
                    )  # retrieve the index of the chunk of the current entry
                    if (
                        index_chunk_start_current_batch is not None
                        and index_chunk
                        >= index_chunk_start_current_batch + int_num_chunks_for_a_batch
                    ):  # if batch has been started
                        __fetch_from_dense_ramtx(l_int_entry_in_a_batch)
                        l_int_entry_in_a_batch = []  # initialize the next batch
                        index_chunk_start_current_batch = None  # reset start

                    """ start the batch """
                    # if start has not been set, set the start of the current batch
                    if index_chunk_start_current_batch is None:  # start the batch
                        index_chunk_start_current_batch = index_chunk

                    # add int_entry to the batch
                    l_int_entry_in_a_batch.append(int_entry)

                if (
                    len(l_int_entry_in_a_batch) > 0
                ):  # if some entries remains unprocessed, flush the buffer
                    __fetch_from_dense_ramtx(l_int_entry_in_a_batch)

            """ return the retrieved data """
            # destroy zarr server
            rtx_fork_safe.terminate_spawned_processes()

            # compose a output value
            output = (
                l_int_entry_of_axis_for_querying,
                l_arr_int_entry_of_axis_not_for_querying,
                l_arr_value,
            )
            #             logger.info( 'ramtx getitem completed' )
            # if 'flag_as_a_worker' is True, send the result or return the result
            if flag_as_a_worker:
                pipe_to_main_thread.send(output)  # send unzipped result back
            else:
                return output

        # load data using multiprocessing
        if (
            self.int_num_cpus > 1 and int_num_entries > 1
        ):  # enter multi-processing mode only more than one entry should be retrieved
            # initialize workers
            int_n_workers = min(
                self.int_num_cpus, int_num_entries
            )  # one thread for distributing records. Minimum numbers of workers for sorting is 1 # the number of workers should not be larger than the number of entries to retrieve.
            l_l_int_entry_for_each_worker = list(
                l
                for l in bk.LIST_Split(
                    l_int_entry, int_n_workers, flag_contiguous_chunk=True
                )
                if len(l) > 0
            )  # retrieve a list of valid work loads for the workers
            int_n_workers = min(
                int_n_workers, len(l_l_int_entry_for_each_worker)
            )  # adjust the number of workers according to the number of distributed workloads

            l_pipes_from_main_process_to_worker = list(
                mp.Pipe() for _ in range(int_n_workers)
            )  # create pipes for sending records to workers # add process for receivers
            l_pipes_from_worker_to_main_process = list(
                mp.Pipe() for _ in range(int_n_workers)
            )  # create pipes for collecting results from workers
            l_processes = list(
                mp.Process(
                    target=__retrieve_data,
                    args=(
                        l_pipes_from_main_process_to_worker[index_worker][1],
                        l_pipes_from_worker_to_main_process[index_worker][0],
                    ),
                )
                for index_worker in range(int_n_workers)
            )  # add a process for distributing fastq records
            for p in l_processes:
                p.start()
            # distribute works
            for index_worker, l_int_entry_for_each_worker in enumerate(
                l_l_int_entry_for_each_worker
            ):  # distribute works # no load balacing for now
                l_pipes_from_main_process_to_worker[index_worker][0].send(
                    l_int_entry_for_each_worker
                )
            # wait until all works are completed
            int_num_workers_completed = 0
            l_output = list(
                [] for i in range(int_n_workers)
            )  # initialize a list that will collect output results
            while (
                int_num_workers_completed < int_n_workers
            ):  # until all works are completed
                for index_worker, cxn in enumerate(l_pipes_from_worker_to_main_process):
                    _, pipe_reciver = cxn  # parse a connection
                    if pipe_reciver.poll():
                        l_output[index_worker] = pipe_reciver.recv()  # collect output
                        int_num_workers_completed += (
                            1  # update the number of completed workers
                        )
                time.sleep(0.1)
            # dismiss workers once all works are completed
            for p in l_processes:
                p.join()

            # ravel retrieved records
            for output in l_output:
                l_int_entry_of_axis_for_querying.extend(output[0])
                l_arr_int_entry_of_axis_not_for_querying.extend(output[1])
                l_arr_value.extend(output[2])
            del output, l_output
        else:  # single thread mode
            (
                l_int_entry_of_axis_for_querying,
                l_arr_int_entry_of_axis_not_for_querying,
                l_arr_value,
            ) = __retrieve_data(l_int_entry, flag_as_a_worker=False)

        return (
            l_int_entry_of_axis_for_querying,
            l_arr_int_entry_of_axis_not_for_querying,
            l_arr_value,
        )

    def get_sparse_matrix(self, l_int_entry, flag_return_as_arrays=False):
        """# 2022-08-30 11:03:14

        get sparse matrix for the given list of integer representations of the entries.

        'l_int_entry' : list of int_entries for query
        'flag_return_as_arrays' : if True, return three arrays and a single list, 'l_int_barcodes', 'l_int_features', 'l_values', 'l_int_num_records'.
                'l_int_barcodes', 'l_int_features', 'l_values' : for building a sparse matrix
                'l_int_num_records' : for building an index
                if False, return a scipy.csr sparse matrix
        """
        (
            l_int_entry_of_axis_for_querying,
            l_arr_int_entry_of_axis_not_for_querying,
            l_arr_value,
        ) = self[
            l_int_entry
        ]  # parse retrieved result

        if len(l_arr_int_entry_of_axis_not_for_querying) > 0:
            # if valid input is available
            # combine the arrays
            arr_int_entry_of_axis_not_for_querying = np.concatenate(
                l_arr_int_entry_of_axis_not_for_querying
            )
            arr_value = np.concatenate(l_arr_value)
            del l_arr_value  # delete intermediate objects

            # compose 'arr_int_entry_of_axis_for_querying'
            arr_int_entry_of_axis_for_querying = np.zeros(
                len(arr_int_entry_of_axis_not_for_querying),
                dtype=self._dtype_of_feature_and_barcode_indices,
            )  # create an empty array
            int_pos = 0
            for int_entry_of_axis_for_querying, a in zip(
                l_int_entry_of_axis_for_querying,
                l_arr_int_entry_of_axis_not_for_querying,
            ):
                n = len(a)
                arr_int_entry_of_axis_for_querying[
                    int_pos : int_pos + n
                ] = int_entry_of_axis_for_querying  # compose 'arr_int_entry_of_axis_for_querying'
                int_pos += n  # update the current position
            if flag_return_as_arrays:
                l_int_num_records = list(
                    len(a) for a in l_arr_int_entry_of_axis_not_for_querying
                )  # when returning arrays instead of a scipy sparse matrix, additionally prepare records that can be utilized for build an index of the data
            del (
                l_int_entry_of_axis_for_querying,
                l_arr_int_entry_of_axis_not_for_querying,
            )  # delete intermediate objects

            # get 'arr_int_barcode' and 'arr_int_feature' based on 'self.is_for_querying_features'
            if self.is_for_querying_features:
                arr_int_barcode = arr_int_entry_of_axis_not_for_querying
                arr_int_feature = arr_int_entry_of_axis_for_querying
            else:
                arr_int_barcode = arr_int_entry_of_axis_for_querying
                arr_int_feature = arr_int_entry_of_axis_not_for_querying
            del (
                arr_int_entry_of_axis_for_querying,
                arr_int_entry_of_axis_not_for_querying,
            )  # delete intermediate objects

            if (
                flag_return_as_arrays
            ):  # if 'flag_return_as_arrays' is True, return data as arrays
                return arr_int_barcode, arr_int_feature, arr_value, l_int_num_records
        else:
            # if input is empty, compose empty inputs
            arr_value, arr_int_barcode, arr_int_feature = [], [], []

        # return data as a sparse matrix
        n_bc, n_ft = (
            (self._int_num_barcodes, self._int_num_features)
            if self._ramdata is None
            else (len(self._ramdata.bc), len(self._ramdata.ft))
        )  # detect whether the current RAMtx has been attached to a RamData and retrieve the number of barcodes and features accordingly
        X = scipy.sparse.csr_matrix(
            scipy.sparse.coo_matrix(
                (arr_value, (arr_int_barcode, arr_int_feature)), shape=(n_bc, n_ft)
            )
        )  # convert count data to a sparse matrix
        return X  # return the composed sparse matrix

    def get_total_num_records(
        self,
        ba=None,
        int_num_entries_for_each_weight_calculation_batch=1000,
        flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=True,
        flag_spawn: Union[bool, None] = None,
    ):
        """# 2022-08-07 01:38:02
        get total number of records in the current RAMtx for the given entries ('ba' filter).
        this function is mainly for the estimation of the total number of records to process for displaying progress information in the progress bar.

        flag_spawn : bool = False # a flag indicating spawning should be used for operations that might not be fork-safe. By default, current object's 'flag_spawn' attribute will be used.
        """
        # set defaule arguments
        if flag_spawn is None:
            flag_spawn = self.flag_spawn
        if ba is None:
            ba = (
                self.ba_filter_axis_for_querying
            )  # if None is given, ba_filter of the currently indexed axis will be used.
            if (
                ba is None
            ):  # if filter is not set or the current RAMtx has not been attached to a RamData object, use the active entries
                ba = (
                    self.ba_active_entries
                )  # if None is given, self.ba_active_entries bitarray will be used.
        # initialize
        # a namespace that can safely shared between function scopes
        ns = {"int_num_records": 0, "l_int_entry_for_weight_calculation_batch": []}

        # check if pre-calculated weights are available
        axis = (
            "features" if self.is_for_querying_features else "barcodes"
        )  # retrieve axis of current ramtx
        flag_weight_available = False  # initialize
        for path_folder in [
            self._path_folder_ramtx,
            self._path_folder_ramtx_modifiable,
        ]:
            if path_folder is not None and zarr_exists(
                f"{path_folder}matrix.{axis}.number_of_records_for_each_entry.zarr/",
                self.fs,
            ):
                path_folder_zarr_weight = f"{path_folder}matrix.{axis}.number_of_records_for_each_entry.zarr/"  # define an existing zarr object path
                flag_weight_available = True
                za_weight = ZarrServer(
                    path_folder_zarr_weight, "r", flag_spawn=flag_spawn
                )  # open zarr object containing weights if available
                break

        def __update_total_num_records():
            """# 2022-08-05 00:56:12
            retrieve indices of the current 'weight_current_batch', calculate weights, and yield a batch
            """
            """ retrieve weights """
            if flag_weight_available and (
                self.mode != "dense"
                or not flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx
            ):  # if weight is available
                # load weight for the batch
                arr_weight = za_weight.get_orthogonal_selection(
                    ns["l_int_entry_for_weight_calculation_batch"]
                )  # retrieve weights
            else:  # if weight is not available
                arr_weight = np.full(
                    len(ns["l_int_entry_for_weight_calculation_batch"]),
                    self.len_axis_not_for_querying,
                )  # if weight is not available, assumes all records are available (number of entries in non-indexed axis) for each entry
            """ update total number of records """
            ns["int_num_records"] += arr_weight.sum()  # update total number of records
            ns[
                "l_int_entry_for_weight_calculation_batch"
            ] = []  # empty the weight calculation batch

        for int_entry in BA.find(
            ba
        ):  # iterate through active entries of the given bitarray
            ns["l_int_entry_for_weight_calculation_batch"].append(
                int_entry
            )  # collect int_entry for the current 'weight_calculation_batch'
            # once 'weight_calculation' batch is full, process the 'weight_calculation' batch
            if (
                len(ns["l_int_entry_for_weight_calculation_batch"])
                == int_num_entries_for_each_weight_calculation_batch
            ):
                __update_total_num_records()  # update total number of records
        if (
            len(ns["l_int_entry_for_weight_calculation_batch"]) > 0
        ):  # if there is remaining entries to be processed
            __update_total_num_records()
        # terminate a spawned process (if exists)
        if flag_weight_available:
            za_weight.terminate()
        return int(ns["int_num_records"])  # return the total number of records

    def batch_generator(
        self,
        ba=None,
        int_num_entries_for_each_weight_calculation_batch=1000,
        int_total_weight_for_each_batch=10000000,
        int_chunk_size_for_checking_boundary=None,
        flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=False,
        flag_spawn: Union[bool, None] = None,
    ):
        """# 2022-12-06 02:51:11
        generate batches of list of integer indices of the active entries in the given bitarray 'ba'.
        Each bach has the following characteristics:
            monotonous: active entries in a batch are in an increasing order
            the total number of records of a batch is around (but not exactly) 'int_total_weight_for_each_batch'

        'ba' : (default None) if None is given, self.ba_active_entries bitarray will be used.
        'int_chunk_size_for_checking_boundary' : if this argument is given, each batch will respect the chunk boundary of the given chunk size so that different batches share the same 'chunk'. setting this argument will override 'int_total_weight_for_each_batch' argument
        'int_total_weight_for_each_batch' : total number of records in a batch.
        'flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx' : when iterating through a dense matrix, interpret the length of the axis not for querying as the total number of records for every entry in the axis for querying. This will be more useful for restricting the memory usage when analysing dense RAMtx matrix.
        flag_spawn : bool = False # a flag indicating spawning should be used for operations that might not be fork-safe. By default, current object's 'flag_spawn' attribute will be used.
        """
        # set defaule arguments
        if flag_spawn is None:
            flag_spawn = self.flag_spawn
        if ba is None:
            ba = (
                self.ba_filter_axis_for_querying
            )  # if None is given, ba_filter of the currently indexed axis will be used.
            if (
                ba is None
            ):  # if filter is not set or the current RAMtx has not been attached to a RamData object, use the active entries
                ba = (
                    self.ba_active_entries
                )  # if None is given, self.ba_active_entries bitarray will be used.
        # initialize
        # a namespace that can safely shared between functions
        ns = {
            "int_accumulated_weight_current_batch": 0,
            "l_int_entry_current_batch": [],
            "l_int_entry_for_weight_calculation_batch": [],
            "index_chunk_end": None,
            "index_batch": 0,
            "int_num_of_previously_returned_entries": 0,
        }  # initialize 'index_batch'

        # check if pre-calculated weights are available
        axis = (
            "features" if self.is_for_querying_features else "barcodes"
        )  # retrieve axis of current ramtx
        flag_weight_available = False  # initialize
        for path_folder in [
            self._path_folder_ramtx,
            self._path_folder_ramtx_modifiable,
        ]:
            if path_folder is not None and zarr_exists(
                f"{path_folder}matrix.{axis}.number_of_records_for_each_entry.zarr/",
                filesystemserver=self.fs,
            ):
                path_folder_zarr_weight = f"{path_folder}matrix.{axis}.number_of_records_for_each_entry.zarr/"  # define an existing zarr object path
                flag_weight_available = True
                za_weight = ZarrServer(
                    path_folder_zarr_weight, "r", flag_spawn=flag_spawn
                )  # open zarr object containing weights if available (open a fork-safe version if 'flag_spawn')
                break

        def __compose_batch():
            """# 2022-08-05 23:34:28
            compose batch from the values available in the namespace 'ns'
            """
            return {
                "index_batch": ns["index_batch"],
                "l_int_entry_current_batch": ns["l_int_entry_current_batch"],
                "int_num_of_previously_returned_entries": ns[
                    "int_num_of_previously_returned_entries"
                ],
                "int_accumulated_weight_current_batch": ns[
                    "int_accumulated_weight_current_batch"
                ],
            }

        def find_batch():
            """# 2022-08-05 00:56:12
            retrieve indices of the current 'weight_current_batch', calculate weights, and yield a batch
            """
            """ retrieve weights """
            if flag_weight_available and (
                self.mode != "dense"
                or not flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx
            ):  # if weight is available and if dense, 'flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx' is False
                # load weight for the batch
                arr_weight = za_weight.get_orthogonal_selection(
                    ns["l_int_entry_for_weight_calculation_batch"]
                )  # retrieve weights
            else:  # if weight is not available
                arr_weight = np.full(
                    len(ns["l_int_entry_for_weight_calculation_batch"]),
                    self.len_axis_not_for_querying,
                )  # if weight is not available, assumes all records are available (number of entries in non-indexed axis) for each entry
            """ search for batch """
            for int_entry, weight in zip(
                ns["l_int_entry_for_weight_calculation_batch"], arr_weight
            ):
                if (
                    ns["index_chunk_end"] is not None
                    and ns["index_chunk_end"]
                    != int_entry // int_chunk_size_for_checking_boundary
                ):  # if the chunk boundary has been set and the boundary has reached
                    yield __compose_batch()  # return a batch
                    # initialize the next batch
                    ns["index_batch"] += 1
                    ns["int_num_of_previously_returned_entries"] += len(
                        ns["l_int_entry_current_batch"]
                    )  # update the total number of entries returned
                    ns["l_int_entry_current_batch"] = []
                    ns["int_accumulated_weight_current_batch"] = 0
                    ns["index_chunk_end"] = None

                # update the current batch
                ns["l_int_entry_current_batch"].append(int_entry)
                ns["int_accumulated_weight_current_batch"] += weight

                # check whether the current batch is full
                if (
                    ns["int_accumulated_weight_current_batch"]
                    >= int_total_weight_for_each_batch
                    and ns["index_chunk_end"] is None
                ):  # a current batch is full, yield the batch # when chunk boundary has not been set
                    if (
                        int_chunk_size_for_checking_boundary is not None
                    ):  # when chunk boundary checking is active
                        ns["index_chunk_end"] = (
                            int_entry // int_chunk_size_for_checking_boundary
                        )  # set the chunk boundary
                    else:
                        yield __compose_batch()  # return a batch
                        # initialize the next batch
                        ns["index_batch"] += 1
                        ns["int_num_of_previously_returned_entries"] += len(
                            ns["l_int_entry_current_batch"]
                        )  # update the total number of entries returned
                        ns["l_int_entry_current_batch"] = []
                        ns["int_accumulated_weight_current_batch"] = 0

            # initialize next 'weight_calculation_batch'
            ns["l_int_entry_for_weight_calculation_batch"] = []

        for int_entry in BA.find(
            ba
        ):  # iterate through active entries of the given bitarray
            ns["l_int_entry_for_weight_calculation_batch"].append(
                int_entry
            )  # collect int_entry for the current 'weight_calculation_batch'
            # once 'weight_calculation' batch is full, process the 'weight_calculation' batch
            if (
                len(ns["l_int_entry_for_weight_calculation_batch"])
                == int_num_entries_for_each_weight_calculation_batch
            ):  # if batch is full
                for (
                    e
                ) in find_batch():  # generate batch from the 'weight_calculation' batch
                    yield e
        if (
            len(ns["l_int_entry_for_weight_calculation_batch"]) > 0
        ):  # process the remaining entries
            for (
                e
            ) in (
                find_batch()
            ):  # generate batch from the last 'weight_calculation_batch'
                yield e
        # return the remaining int_entries as the last batch (if available)
        if len(ns["l_int_entry_current_batch"]) > 0:
            yield __compose_batch()  # return a batch

        # terminate a spawned process (if exists)
        if flag_weight_available:
            za_weight.terminate()


""" a class for representing a layer of RamData """


class RamDataLayer:
    """# 2022-09-01 01:24:07
    A class for interactions with a pair of RAMtx objects of a count matrix.

    'path_folder_ramdata' : location of RamData
    'int_num_cpus' : number of CPUs for RAMtx objects
    'mode' : file mode. 'r' for read-only mode and 'a' for mode allowing modifications
    'flag_is_read_only' : read-only status of RamData
    'path_folder_ramdata_mask' : a local (local file system) path to the mask of the RamData object that allows modifications to be written without modifying the source. if a valid local path to a mask is given, all modifications will be written to the mask

    === arguments for combined layer object ===
    l_layer : a layer to to intialize a combined layer

    === Synchronization across multiple processes ===
    zarrspinlockserver : Union[ None, ZarrSpinLockServer ] = None # a ZarrSpinLockServer object for synchronization of methods of the current object.
    """

    def __init__(
        self,
        path_folder_ramdata,
        name_layer,
        l_layer: Union[list, tuple, None] = None,
        ramdata=None,
        dtype_of_feature_and_barcode_indices=np.int32,
        dtype_of_values=np.float64,
        int_num_cpus=1,
        verbose=False,
        mode="a",
        path_folder_ramdata_mask=None,
        flag_is_read_only=False,
        zarrspinlockserver: Union[None, ZarrSpinLockServer] = None,
    ):
        """# 2022-07-31 14:33:46"""
        # harded coded settings
        self._set_valid_modes = {
            "dense",
            "dense_for_querying_barcodes",
            "dense_for_querying_features",
            "sparse_for_querying_barcodes",
            "sparse_for_querying_features",
        }  # define a set of valid modes

        # set attributes
        self._path_folder_ramdata = path_folder_ramdata
        self._name_layer = name_layer
        self._path_folder_ramdata_layer = f"{path_folder_ramdata}{name_layer}/"
        self._ramdata = ramdata
        self._mode = mode
        self.verbose = verbose
        self._int_num_cpus = int_num_cpus
        self._l_layer = l_layer
        self._path_folder_ramdata_mask = path_folder_ramdata_mask
        if (
            path_folder_ramdata_mask is not None
        ):  # set path to the mask of the layer if ramdata mask has been given
            self._path_folder_ramdata_layer_mask = (
                f"{self._path_folder_ramdata_mask}{name_layer}/"
            )
        self._flag_is_read_only = flag_is_read_only
        self._dtype_of_values = dtype_of_values
        self._dtype_of_feature_and_barcode_indices = (
            dtype_of_feature_and_barcode_indices
        )

        # load a zarr spin lock server
        self._zsls = (
            zarrspinlockserver
            if isinstance(zarrspinlockserver, ZarrSpinLockServer)
            else None
        )

        """ write metadata if RamDataLayer is newly initialized """
        if not zarr_exists(self._path_folder_ramdata_layer):
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.acquire_lock(
                    f"{self._path_folder_ramdata_layer}.zattrs.lock"
                )

            self._root = zarr.open(self._path_folder_ramdata_layer, "a")
            # compose metadata
            self._dict_metadata = {
                "set_modes": [],  # no available modes
                "version": _version_,
            }
            self._root.attrs[
                "dict_metadata"
            ] = self._dict_metadata  # write the metadata

            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.release_lock(
                    f"{self._path_folder_ramdata_layer}.zattrs.lock"
                )
        # read metadata
        self._root = zarr.open(self._path_folder_ramdata_layer, "a")
        self._dict_metadata = self._root.attrs["dict_metadata"]  # retrieve the metadata

        # retrieve filters from the axes
        ba_filter_features = ramdata.ft.filter if ramdata is not None else None
        ba_filter_barcodes = ramdata.bc.filter if ramdata is not None else None

        # set filters of the current layer
        self.ba_filter_features = ba_filter_features
        self.ba_filter_barcodes = ba_filter_barcodes

        # load ramtx
        self._load_ramtx_objects()

    @property
    def path_folder(self):
        """# 2023-04-12 17:19:28"""
        return self._path_folder_ramdata

    def _ipython_key_completions_(self):
        """# 2023-01-21 14:50:07
        (ipython integration) method for supporting autocompletion of columns
        """
        return list(self.modes)

    @property
    def locking_server(self):
        """# 2022-12-23 00:02:37
        return 'ZarrSpinLockServer' object
        """
        return self._zsls

    @locking_server.setter
    def locking_server(self, locking_server_new):
        """# 2022-12-23 00:02:43"""
        self._zsls = (
            locking_server_new  # set 'ZarrSpinLockServer' of the current object
        )

        # propagate 'locking_server' change to the loaded rtx objects
        for rtx in self:
            rtx.locking_server = locking_server_new

    @property
    def path_folder_ramdata_layer(self):
        """# 2022-12-14 18:57:27
        return the folder where the RamDataLayer object resides
        """
        return self._path_folder_ramdata_layer

    @property
    def is_combined(self):
        """# 2022-09-01 01:29:25
        return True if current RamDataLayer is in 'combined' mode
        """
        return self._l_layer is not None

    def _load_ramtx_objects(self):
        """# 2022-08-01 10:57:28
        load all ramtx present in the layer
        """
        # load RAMtx objects without filters
        # define arguments for opening RAMtx objects
        dict_kwargs = {
            "ramdata": self._ramdata,
            "dtype_of_feature_and_barcode_indices": self._dtype_of_feature_and_barcode_indices,
            "dtype_of_values": self._dtype_of_values,
            "int_num_cpus": self._int_num_cpus,
            "verbose": self.verbose,
            "flag_debugging": False,
            "mode": self._mode,
            "flag_is_read_only": self._flag_is_read_only,
            "l_rtx": None,
            "zarrspinlockserver": self._zsls,
        }
        # load ramtx
        for mode in self.modes:  # iterate through each mode
            # retrieve directory of the mask
            dict_kwargs["path_folder_ramtx_mask"] = (
                f"{self._path_folder_ramdata_layer_mask}{mode}/"
                if self._mask_available
                else None
            )
            if self.is_combined:
                # %% COMBINED %%
                dict_kwargs["l_rtx"] = list(
                    None if layer is None else layer[mode] for layer in self._l_layer
                )  # retrieve list of rtx objects for the current mode
            if not hasattr(
                self, f"ramtx_{mode}"
            ):  # if the ramtx object of the current mode has not been load
                if "dense_for_querying_" in mode:
                    rtx = RAMtx(
                        f"{self._path_folder_ramdata_layer}dense/",
                        is_for_querying_features=mode.rsplit("dense_for_querying_", 1)[
                            1
                        ]
                        == "features",
                        **dict_kwargs,
                    )  # open dense ramtx in querying_features/querying_barcodes modes
                else:
                    rtx = RAMtx(
                        f"{self._path_folder_ramdata_layer}{mode}/", **dict_kwargs
                    )
                setattr(self, f"ramtx_{mode}", rtx)  # set ramtx as an attribute

        # set filters of the loaded RAMtx objects
        self.ba_filter_features = self.ba_filter_features
        self.ba_filter_barcodes = self.ba_filter_barcodes

    def __repr__(self):
        """# 2022-07-31 01:03:21"""
        return f"<RamDataLayer object '{self.name}' containing {self.modes} RAMtx objects\n\tRamDataLayer path: {self._path_folder_ramdata_layer}>"

    @property
    def name(self):
        """# 2022-07-31 01:10:00
        return the name of the layer
        """
        return self._name_layer

    """ <Methods for Synchronization> """

    @property
    def use_locking(self):
        """# 2022-12-12 02:45:43
        return True if a spin lock algorithm is being used for synchronization of operations on the current object
        """
        return self._zsls is not None

    @property
    def metadata(self):
        """# 2022-07-21 02:38:31"""
        return self.get_metadata()

    def get_metadata(self):
        """# 2022-12-13 02:00:26
        read metadata with file-locking
        """
        path_folder = (
            self._path_folder_ramdata_layer
        )  # retrieve path to the zarr object
        if (
            self.use_locking
        ):  # when locking has been enabled, read metadata from the storage, and update the metadata currently loaded in the memory
            # %% FILE LOCKING %%
            self._zsls.wait_lock(
                f"{path_folder}.zattrs.lock/"
            )  # wait until a lock is released
            self._dict_metadata = self._zsls.zms.get_metadata(
                path_folder, "dict_metadata"
            )  # retrieve metadata from the storage, and update the metadata stored in the object
        elif not hasattr(
            self, "_dict_metadata"
        ):  # when locking is not used but the metadata has not been loaded, read the metadata without using the locking algorithm
            self._dict_metadata = self._root.attrs[
                "dict_metadata"
            ]  # retrieve 'dict_metadata' from the storage
        return self._dict_metadata  # return the metadata

    def set_metadata(self, dict_metadata: dict):
        """# 2022-12-11 22:08:05
        write metadata with file-locking
        """
        path_folder = (
            self._path_folder_ramdata_layer
        )  # retrieve path to the zarr object
        if (
            self._flag_is_read_only
        ):  # save metadata only when it is not in the read-only mode
            return
        self._dict_metadata = dict_metadata  # update metadata stored in the memory
        if (
            self._zsls is None
        ):  # if locking is not used, return previously loaded metadata
            self._root.attrs["dict_metadata"] = self._dict_metadata
        else:  # when locking has been enabled
            self._zsls.acquire_lock(f"{path_folder}.zattrs.lock/")  # acquire a lock
            self._zsls.zms.set_metadata(
                path_folder, "dict_metadata", self._dict_metadata
            )  # write metadata to the storage
            self._zsls.release_lock(f"{path_folder}.zattrs.lock/")  # release the lock

    def update_metadata(
        self,
        dict_metadata_to_be_updated: dict = dict(),
        l_mode_to_be_deleted: list = [],
        l_mode_to_be_added: list = [],
    ):
        """# 2022-12-14 11:24:50
        write metadata with file-locking

        dict_metadata_to_be_updated : dict # a dictionarty for updating 'dict_metadata' of the current object
        l_mode_to_be_deleted : list = [ ] # list of modes to be deleted
        l_mode_to_be_added : list = [ ] # list of modes to be added
        """
        if (
            self._flag_is_read_only
        ):  # update the metadata only when it is not in the read-only mode
            return
        path_folder = (
            self._path_folder_ramdata_layer
        )  # retrieve path to the zarr object

        def __update_dict_metadata(
            dict_metadata: dict,
            dict_metadata_to_be_updated: dict,
            l_mode_to_be_deleted: list = [],
            l_mode_to_be_added: list = [],
        ):
            """# 2022-12-13 19:30:27
            update dict_metadata with dict_metadata_to_be_updated and return the updated dict_metadata
            """
            # update 'dict_metadata'
            dict_metadata.update(dict_metadata_to_be_updated)

            # delete modes from the 'dict_metadata'
            for name_mode in l_mode_to_be_deleted:
                if name_mode in dict_metadata["set_modes"]:
                    dict_metadata["set_modes"].remove(name_mode)

            # add modes to the 'dict_metadata'
            for name_mode in l_mode_to_be_added:
                if name_mode in self._set_valid_modes:  # check validity of 'name_mode'
                    dict_metadata["set_modes"].append(name_mode)
            dict_metadata["set_modes"] = list(set(dict_metadata["set_modes"]))

            return dict_metadata

        if (
            not self.use_locking
        ):  # if locking is not used, return previously loaded metadata
            self._dict_metadata = __update_dict_metadata(
                self._dict_metadata,
                dict_metadata_to_be_updated,
                l_mode_to_be_deleted,
                l_mode_to_be_added,
            )  # update 'self._dict_metadata' with 'dict_metadata_to_be_updated'
            self._root.attrs["dict_metadata"] = self._dict_metadata
        else:  # when locking has been enabled
            self._zsls.acquire_lock(f"{path_folder}.zattrs.lock/")  # acquire a lock

            self._dict_metadata = self._zsls.zms.get_metadata(
                path_folder, "dict_metadata"
            )  # read metadata from the storage and update the metadata
            self._dict_metadata = __update_dict_metadata(
                self._dict_metadata,
                dict_metadata_to_be_updated,
                l_mode_to_be_deleted,
                l_mode_to_be_added,
            )  # update 'self._dict_metadata' with 'dict_metadata_to_be_updated'
            self._zsls.zms.set_metadata(
                path_folder, "dict_metadata", self._dict_metadata
            )  # write metadata to the storage

            self._zsls.release_lock(f"{path_folder}.zattrs.lock/")  # release the lock

    def _save_metadata_(self):
        """# 2022-07-20 10:31:39
        save metadata of the current ZarrDataFrame
        """
        if (
            not self._flag_is_read_only
        ):  # save metadata only when it is not in the read-only mode
            # save dict_metadata
            if self.use_locking:  # %% FILE LOCKING %%
                self.set_metadata(self._dict_metadata)
            else:
                self._root.attrs[
                    "dict_metadata"
                ] = self._dict_metadata  # update metadata

    """ </Methods for Synchronization> """

    @property
    def _mask_available(self):
        """# 2022-07-30 18:38:30"""
        return self._path_folder_ramdata_mask is not None

    @property
    def modes(self):
        """# 2022-09-01 02:02:54
        return a subst of {'dense', 'dense_for_querying_barcodes', 'dense_for_querying_features', 'sparse_for_querying_barcodes', 'sparse_for_querying_features'}
        """
        modes = set(self._dict_metadata["set_modes"])
        # add modes of the components
        if self.is_combined:
            # %% COMBINED %%
            for layer in self._l_layer:
                if layer is not None:
                    modes.update(layer.modes)  # update modes
        return modes

    @property
    def int_num_cpus(self):
        """# 2022-07-21 23:22:24"""
        return self._int_num_cpus

    @int_num_cpus.setter
    def int_num_cpus(self, val):
        """# 2022-07-21 23:22:24"""
        self._int_num_cpus = max(1, int(val))  # set integer values
        for rtx in self:  # iterate through ramtxs
            rtx.int_num_cpus = (
                self._int_num_cpus
            )  # update 'int_num_cpus' attributes of RAMtxs

    @property
    def int_num_features(self):
        """# 2022-06-28 21:39:20
        return the number of features
        """
        return self[
            list(self.modes)[0]
        ]._int_num_features  # return an attribute of the first ramtx of the current layer

    @property
    def int_num_barcodes(self):
        """# 2022-06-28 21:39:20
        return the number of features
        """
        return self[
            list(self.modes)[0]
        ]._int_num_barcodes  # return an attribute of the first ramtx of the current layer

    @property
    def int_num_records(self):
        """# 2022-06-28 21:39:20
        return the number of features
        """
        return self[
            list(self.modes)[0]
        ]._int_num_records  # return an attribute of the first ramtx of the current layer

    @property
    def ba_filter_features(self):
        """# 2022-06-26 01:31:24"""
        return self._ba_filter_features

    @ba_filter_features.setter
    def ba_filter_features(self, ba_filter):
        """# 2022-06-26 01:31:24"""
        # set/update the filter for the associated RAMtx objects
        self._ba_filter_features = ba_filter
        for rtx in self:
            rtx.ba_filter_features = ba_filter

    @property
    def ba_filter_barcodes(self):
        """# 2022-06-26 01:31:24"""
        return self._ba_filter_barcodes

    @ba_filter_barcodes.setter
    def ba_filter_barcodes(self, ba_filter):
        """# 2022-06-26 01:31:24"""
        # set/update the filter for the associated RAMtx objects
        self._ba_filter_barcodes = ba_filter
        for rtx in self:
            rtx.ba_filter_barcodes = ba_filter

    def __contains__(self, mode):
        """# 2022-12-17 08:32:04
        check whether mode 'x' is available in the layer
        """
        return hasattr(self, f"ramtx_{mode}")

    def __iter__(self):
        """# 2022-07-30 18:42:50
        iterate through ramtx of the modes available in the layer
        """
        return iter(
            list(getattr(self, attr) for attr in vars(self) if "ramtx_" == attr[:6])
        )  # return ramtx object that has been loaded in the current layer

    def select_ramtx(self, ba_entry_bc, ba_entry_ft):
        """# 2023-01-21 16:02:27
        select appropriate ramtx based on the queryed barcode and features, given as a bitarray filters 'ba_entry_bc', 'ba_entry_ft'
        """
        # count the number of valid queried entries
        int_num_entries_queried_bc = ba_entry_bc.count()
        int_num_entries_queried_ft = ba_entry_ft.count()

        # detect and handle the cases when one of the axes is empty
        if int_num_entries_queried_bc == 0 or int_num_entries_queried_ft == 0:
            if self.verbose:
                logger.warning(
                    f"currently queried view is (barcode x features) {int_num_entries_queried_bc} x {int_num_entries_queried_ft}. please change the filter or queries in order to retrieve a valid count data. For operations that do not require count data, ignore this warning."
                )

        # choose which ramtx object to use
        flag_use_ramtx_for_querying_feature = int_num_entries_queried_bc / len(
            ba_entry_bc
        ) >= int_num_entries_queried_ft / len(
            ba_entry_ft
        )  # select which axis to use. if a proportion of barcodes that have been selected is larger than that of features, use ramtx for querying 'features' to reduce file I/O

        rtx = self.get_ramtx(
            flag_is_for_querying_features=flag_use_ramtx_for_querying_feature
        )  # retrieve ramtx
        if rtx is None:
            return self[list(self.modes)[0]]  # return any ramtx as a fallback
        return rtx

    def get_ramtx(
        self,
        flag_is_for_querying_features=True,
        flag_prefer_dense=False,
        set_int_index_component_to_exclude: Union[None, set] = None,
    ):
        """# 2022-09-20 12:00:56
        retrieve ramtx for querying feature/barcodes

        flag_is_for_querying_features = True # if True, return RAMtx that can be queried by features
        flag_prefer_dense = False # prefer dense matrix over sparse matrix
        set_int_index_component_to_exclude : Union[ None, set ] = None # set of integer indices of the components to exclude.
            the intended usage of this argument is to exclude RAMtx of the component that will be used as a reference
        """
        # handle combined RAMtx
        if self.is_combined:
            # %% COMBINED %%
            # create the ramtx
            # set default 'set_int_index_component_to_exclude'
            if set_int_index_component_to_exclude is None:
                set_int_index_component_to_exclude = set()
            l_rtx = list(
                None
                if int_index_component in set_int_index_component_to_exclude
                or layer is None
                else layer.get_ramtx(
                    flag_is_for_querying_features=flag_is_for_querying_features,
                    flag_prefer_dense=flag_prefer_dense,
                )
                for int_index_component, layer in enumerate(self._l_layer)
            )  # retrieve list of rtx with the given settings
            mode = "___".join(
                list("None" if rtx is None else rtx.mode for rtx in l_rtx)
            )  # retrieve the name of 'mode' for the current ramtx
            # define arguments for opening a RAMtx object
            dict_kwargs = {
                "ramdata": self._ramdata,
                "dtype_of_feature_and_barcode_indices": self._dtype_of_feature_and_barcode_indices,
                "dtype_of_values": self._dtype_of_values,
                "int_num_cpus": self._int_num_cpus,
                "verbose": self.verbose,
                "flag_debugging": False,
                "mode": self._mode,
                "path_folder_ramtx_mask": f"{self._path_folder_ramdata_layer_mask}{mode}/"
                if self._mask_available
                else None,
                "flag_is_read_only": self._flag_is_read_only,
                "l_rtx": l_rtx,  # retrieve list of rtx objects for the current mode
                "zarrspinlockserver": self._zsls,
            }
            rtx = RAMtx(f"{self._path_folder_ramdata_layer}{mode}/", **dict_kwargs)
            # apply filters
            rtx.ba_filter_features = self.ba_filter_features
            rtx.ba_filter_barcodes = self.ba_filter_barcodes
            setattr(
                self, f"ramtx_{mode}", rtx
            )  # set the ramtx as an attribute to update the filter of the ramtx
            return rtx

        mode_dense = f"dense_for_querying_{'features' if flag_is_for_querying_features else 'barcodes'}"  # retrieve mode name for dense ramtx based on 'flag_is_for_querying_features'
        mode_sparse = f"sparse_for_querying_{'features' if flag_is_for_querying_features else 'barcodes'}"  # retrieve mode name for sparse ramtx based on 'flag_is_for_querying_features'
        for mode in (
            [mode_dense, mode_sparse]
            if flag_prefer_dense
            else [mode_sparse, mode_dense]
        ):  # search ramtx considering 'flag_prefer_dense'
            if mode in self:
                return self[mode]
        if self.verbose:
            logger.info(
                f"ramtx for querying {'features' if flag_is_for_querying_features else 'barcodes'} efficiently is not available for layer {self.name}, containing the following modes: {self.modes}"
            )
        return None

    def __getitem__(self, mode):
        """# 2022-09-01 09:11:56"""
        if mode in self:  # if a given mode is available
            if hasattr(self, f"ramtx_{mode}"):  # if a given mode has been loaded
                return getattr(
                    self, f"ramtx_{mode}"
                )  # return the ramtx of the given mode

    def __delitem__(self, mode):
        """# 2022-12-15 00:13:08"""
        # ignore if combined mode is active (ramtx of component RamData should not be deleted from the combined RamData)
        if self.is_combined:
            return
        # ignore if current mode is 'read-only'
        if self._mode == "r":
            return
        if mode in self:  # if a given mode is available
            if hasattr(self, f"ramtx_{mode}"):  # if a given mode has been loaded
                # delete from memory
                if "dense" in mode:  # handle 'dense' mode
                    l_mode_to_be_deleted = [
                        "dense_for_querying_features",
                        "dense_for_querying_barcodes",
                        "dense",
                    ]
                    mode = "dense"
                else:
                    l_mode_to_be_deleted = [mode]

                # delete from the memory
                for mode_to_delete in l_mode_to_be_deleted:
                    delattr(self, f"ramtx_{mode_to_delete}")

                self.update_metadata(
                    l_mode_to_be_deleted=l_mode_to_be_deleted
                )  # update metadata

                # delete from the storage
                filesystem_operations("rm", f"{self._path_folder_ramdata_layer}{mode}/")

    def terminate_spawned_processes(self):
        """# 2022-12-06 19:22:22
        terminate spawned processes from the RAMtx object containined in the current layer
        """
        for rtx in self:  # for each RAMtx object
            rtx.terminate_spawned_processes()  # terminate spawned processes from the RAMtx object


""" class for storing RamData """


class RamData:
    """# 2023-05-06 11:35:48 
    This class provides frameworks for single-cell transcriptomic/genomic data analysis, utilizing RAMtx data structures, which is backed by Zarr persistant arrays.
    Extreme lazy loading strategies used by this class allows efficient parallelization of analysis of single cell data with minimal memory footprint, loading only essential data required for analysis.

    'path_folder_ramdata' : a local folder directory or a remote location (https://, s3://, etc.) containing RamData object
    'int_num_cpus' : number of CPUs (processes) to use to distribute works.
    int_num_cpus_for_updating_metadata : int = 10, # the number of CPUs for updating metadata (ZarrDataFrame)
    'int_num_cpus_for_fetching_data' : number of CPUs (processes) for individual RAMtx object for retrieving data from the data source.
    'int_index_str_rep_for_barcodes', 'int_index_str_rep_for_features' : a integer index for the column for the string representation of 'barcodes'/'features' in the string Zarr object (the object storing strings) of 'barcodes'/'features'
    'dict_kw_zdf' : settings for 'Axis' metadata ZarrDataFrame
    'dict_kw_view' : settings for 'Axis' object for creating a view based on the active filter.
    'mode' : file mode. 'r' for read-only mode and 'a' for mode allowing modifications
    'path_folder_ramdata_mask' : the LOCAL file system path where the modifications of the RamData ('MASK') object will be saved and retrieved. If this attribute has been set, the given RamData in the the given 'path_folder_ramdata' will be used as READ-ONLY. For example, when RamData resides in the HTTP server, data is often read-only (data can be only fetched from the server, and not the other way around). However, by giving a local path through this argument, the read-only RamData object can be analyzed as if the RamData object can be modified. This is possible since all the modifications made on the input RamData will be instead written to the local RamData object 'mask' and data will be fetced from the local copy before checking the availability in the remote RamData object.

    === batch generation ===
    'int_num_entries_for_each_weight_calculation_batch' : the number of entries in a small batch for generating load-balanced batches.
    'int_total_weight_for_each_batch' : the argument controlling total number of records to be processed in each batch (and thus for each process for parallelized works). it determines memory usage/operation efficiency. higher weight will lead to more memory usage but more operation efficiency, and vice versa
    'flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx' : when iterating through a dense matrix, interpret the length of the axis not for querying as the total number of records for every entry in the axis for querying. This will be more useful for restricting the memory usage when analysing dense RAMtx matrix.

    === Combined RamData ===
    l_ramdata : Union[ List[ RamData ], None ] = None # list of RamData objects to combine.
    flag_combined_ramdata_barcodes_shared_across_ramdata : bool = False # True if barcodes are shared across RamData objects. If barcodes are unique and not shared across RamData objects (which usually are), set this flag to False
    flag_combined_ramdata_features_shared_across_ramdata : bool = True # True if features are shared across RamData objects. If features are shared across RamData objects (which usually are), set this flag to True
    flag_check_combined_type : bool = False # flag for checking combined type ('interleaved/stacked') across the 'barcodes/features' axis objeccts of the given list of ramdata objects.
    index_ramdata_source_for_combined_barcodes_shared_across_ramdata : int = 0 # index of ramdata component that will be used to retrieve data of 'barcodes' axis objects contain duplicated records
    index_ramdata_source_for_combined_features_shared_across_ramdata : int = 0 # index of ramdata component that will be used to retrieve data of 'features' axis objects contain duplicated records

        === Reference-based analysis ===
        int_index_component_reference : Union[ int, None ] = None # if an integer is given and 'combined' mode is being used, use the component as the 'default' reference component.

    === Amazon S3/other file remote system ===
    path_folder_temp_local_default_for_remote_ramdata : str = '/tmp/' # a default local temporary folder where the temporary output files will be saved and processed before being uploaded to the remote location, where RamData resides remotely, which makes the file system operations more efficient.
    dict_kwargs_credentials_s3 : dict = dict( ) # credentials for Amazon S3 object. By default, credentials will be retrieved from the default location.

    === Synchronization across multiple processes and (remote) devices analyzing the current RamData (multiple 'researchers') ===
    flag_enable_synchronization_through_locking : bool = True # if True, enable sycnrhonization of modifications on RamData using file-system-based locking.
    flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock : bool = False # if True, does not wait and raise 'RuntimeError' when a modification of a RamData cannot be made due to the resource that need modification is temporarily unavailable, locked by other processes
    float_second_to_wait_before_checking_availability_of_a_spin_lock : float = 0.5 # number of seconds to wait before repeatedly checking the availability of a spin lock if the lock has been acquired by other operations.
    flag_spawn : Union[ None, bool ] = None # by default, automatically determines whether 'spawn' method should be used during multiprocessing. When Zarr objects are located remotely, 'spawn' method will be used.

    === AnnDataContainer ===
    flag_load_anndata_container : bool = False # load anndata container to load/save anndata objects stored in the curren RamData object
    'flag_enforce_name_adata_with_only_valid_characters' : enforce valid characters in the name of AnnData
    """

    def __init__(
        self,
        path_folder_ramdata: str,
        l_ramdata: Union[list, tuple, None] = None,
        ramdata_composite=None,
        flag_combined_ramdata_barcodes_shared_across_ramdata: bool = False,
        flag_combined_ramdata_features_shared_across_ramdata: bool = True,
        flag_check_combined_type: bool = False,
        index_ramdata_source_for_combined_barcodes_shared_across_ramdata: int = 0,
        index_ramdata_source_for_combined_features_shared_across_ramdata: int = 0,
        name_layer: Union[None, str] = "raw",
        int_num_cpus: int = 64,
        int_num_cpus_for_updating_metadata: int = 10,
        int_num_cpus_for_fetching_data: int = 1,
        dtype_of_feature_and_barcode_indices=np.int32,
        dtype_of_values=np.float64,
        int_index_str_rep_for_barcodes: int = 0,
        int_index_str_rep_for_features: int = 1,
        int_num_entries_for_each_weight_calculation_batch: int = 2000,
        int_total_weight_for_each_batch: int = 20000000,
        flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx: bool = False,
        mode: str = "a",
        path_folder_ramdata_mask: Union[str, None] = None,
        dict_kw_zdf: dict = {
            "flag_retrieve_categorical_data_as_integers": False,
            "flag_load_data_after_adding_new_column": False,
            "flag_enforce_name_col_with_only_valid_characters": False,
        },
        dict_kw_view: dict = {
            "float_min_proportion_of_active_entries_in_an_axis_for_using_array": 0.1,
            "dtype": np.int32,
        },
        flag_load_anndata_container: bool = False,
        flag_enforce_name_adata_with_only_valid_characters: bool = True,
        int_index_component_reference: Union[int, None] = None,
        path_folder_temp_local_default_for_remote_ramdata: str = "/tmp/",
        dict_kwargs_credentials_s3: dict = dict(),
        flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock: bool = False,
        float_second_to_wait_before_checking_availability_of_a_spin_lock: float = 0.05,
        flag_enable_synchronization_through_locking: bool = True,
        flag_spawn: Union[None, bool] = None,
        verbose: bool = True,
        flag_debugging: bool = False,
    ):
        """# 2023-04-12 17:37:33"""
        """ hard-coded settings  """
        # define a set of picklable models :
        self._set_type_model_picklable = {
            "ipca",
            "hdbscan",
            "knn_classifier",
            "knn_embedder",
            "knngraph",
            "knnindex",
        }
        self._set_type_model_keras_model = {
            "deep_learning.keras.classifier",
            "deep_learning.keras.embedder",
        }  # model containing keras model. keras model can be retrieved from the 'dict_model' using 'dl_model' as a key

        """ soft-coded settings """
        # changable settings (settings that can be changed anytime in the lifetime of a RamData object)
        self._dict_kwargs_credentials_s3 = (
            dict_kwargs_credentials_s3  # save 'dict_kwargs_credentials_s3'
        )
        self._flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock = flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock
        self._float_second_to_wait_before_checking_availability_of_a_spin_lock = (
            float_second_to_wait_before_checking_availability_of_a_spin_lock
        )
        self.verbose = verbose
        self.flag_debugging = flag_debugging
        # the number of processes to be used
        self._int_num_cpus = int_num_cpus
        # batch-generation associated settings, which can be changed later
        self.int_num_entries_for_each_weight_calculation_batch = (
            int_num_entries_for_each_weight_calculation_batch
        )
        self.int_total_weight_for_each_batch = int_total_weight_for_each_batch
        self.flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx = flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx

        # default settings
        # handle input object paths
        if (
            path_folder_ramdata[-1] != "/"
        ):  # add '/' at the end of path to indicate it is a directory
            path_folder_ramdata += "/"
        if (
            "://" not in path_folder_ramdata
        ):  # do not call 'os.path.abspath' on remote path
            path_folder_ramdata = (
                os.path.abspath(path_folder_ramdata) + "/"
            )  # retrieve abs path
        if (
            path_folder_ramdata_mask is not None
        ):  # if 'path_folder_ramdata_mask' is given, assumes it is a local path
            path_folder_ramdata_mask = (
                os.path.abspath(path_folder_ramdata_mask) + "/"
            )  # retrieve abs path

        # set attributes
        self._flag_enable_synchronization_through_locking = (
            flag_enable_synchronization_through_locking
        )
        self._mode = mode
        self._path_folder_ramdata = path_folder_ramdata

        """ set multiprocessing methods """
        if flag_spawn is None:
            flag_spawn = self.is_remote
        self._flag_spawn = flag_spawn

        # set attributes
        self._path_folder_ramdata_mask = path_folder_ramdata_mask
        self._int_num_cpus_for_updating_metadata = int_num_cpus_for_updating_metadata
        self._int_num_cpus_for_fetching_data = int_num_cpus_for_fetching_data
        self._dtype_of_feature_and_barcode_indices = (
            dtype_of_feature_and_barcode_indices
        )
        self._dtype_of_values = dtype_of_values
        self._path_folder_temp_local_default_for_remote_ramdata = (
            path_folder_temp_local_default_for_remote_ramdata
        )
        # combined ramdata
        self._l_ramdata = l_ramdata
        self._ramdata_composite = ramdata_composite
        self._flag_combined_ramdata_barcodes_shared_across_ramdata = (
            flag_combined_ramdata_barcodes_shared_across_ramdata
        )
        self._flag_combined_ramdata_features_shared_across_ramdata = (
            flag_combined_ramdata_features_shared_across_ramdata
        )
        # combined ramdata setting, which can be changed later
        self._index_ramdata_source_for_combined_barcodes_shared_across_ramdata = (
            index_ramdata_source_for_combined_barcodes_shared_across_ramdata
        )
        self._index_ramdata_source_for_combined_features_shared_across_ramdata = (
            index_ramdata_source_for_combined_features_shared_across_ramdata
        )
        self._int_index_component_reference = (
            int_index_component_reference  # set the index of the reference component
        )
        if self.is_combined:
            # %% COMBINED %%
            for ram in self._l_ramdata:
                ram._ramdata_composite = self  # give component RamData access to the current composite RamData

        """ check read-only status of the given RamData """
        try:
            zarr.open(f"{self._path_folder_ramdata}modification.test.zarr/", "w")
            self._flag_is_read_only = False
        except:
            # if test zarr data cannot be written to the source, consider the given RamData object as read-only
            self._flag_is_read_only = True  # indicates current RamData object is read-only (however, Mask can be give, and RamData can be modified by modifying the mask)
            if (
                self._path_folder_ramdata_mask is None
            ):  # if mask is not given, automatically change the mode to 'r'
                self._mode = "r"  # indicate current RamData cannot be modified
                if self.verbose:
                    logger.info(
                        'The current RamData object cannot be modified yet no mask location is given. Therefore, the current RamData object will be "read-only"'
                    )

        """ set 'path_folder_temp' """
        path_folder_temp = (
            f"{path_folder_temp_local_default_for_remote_ramdata}tmp_{bk.UUID( )}/"
            if self._path_folder_ramdata_modifiable is None
            or is_remote_url(self._path_folder_ramdata_modifiable)
            else f"{self._path_folder_ramdata_modifiable}temp/"
        )  # define a temporary directory in the current working directory if modifiable RamData resides locally. if the modifiable RamData resides remotely or cannot be modified, create a temp folder in the 'path_folder_temp_local_default_for_remote_ramdata' use the folder as a the temporary folder
        self._path_folder_temp = (
            path_folder_temp  # set path of the temporary folder as an attribute
        )

        """ start a spin lock server (if 'flag_enable_synchronization_through_locking' is True) """
        self._zsls = (
            ZarrSpinLockServer(
                flag_spawn=self.flag_spawn,
                dict_kwargs_credentials_s3=dict_kwargs_credentials_s3,
                flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock=flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock,
                float_second_to_wait_before_checking_availability_of_a_spin_lock=float_second_to_wait_before_checking_availability_of_a_spin_lock,
            )
            if flag_enable_synchronization_through_locking
            else None
        )

        # initialize axis objects
        dict_setting = dict(
            flag_check_combined_type=flag_check_combined_type,
            ba_filter=None,
            ramdata=self,
            dict_kw_zdf=dict_kw_zdf,
            dict_kw_view=dict_kw_view,
            verbose=verbose,
            mode=self._mode,
            path_folder_mask=self._path_folder_ramdata_mask,
            flag_is_read_only=self._flag_is_read_only,
            zarrspinlockserver=self._zsls,
            int_num_cpus=self.int_num_cpus_for_updating_metadata,
            flag_spawn=self.flag_spawn,
        )
        self.bc = RamDataAxis(
            path_folder_ramdata,
            "barcodes",
            index_ax_data_source_when_interleaved=index_ramdata_source_for_combined_barcodes_shared_across_ramdata,
            flag_is_interleaved=flag_combined_ramdata_barcodes_shared_across_ramdata,
            int_index_str_rep=int_index_str_rep_for_barcodes,
            l_ax=list(ram.bc for ram in self._l_ramdata)
            if self._l_ramdata is not None
            else None,
            **dict_setting,
        )
        self.ft = RamDataAxis(
            path_folder_ramdata,
            "features",
            index_ax_data_source_when_interleaved=index_ramdata_source_for_combined_features_shared_across_ramdata,
            flag_is_interleaved=flag_combined_ramdata_features_shared_across_ramdata,
            int_index_str_rep=int_index_str_rep_for_features,
            l_ax=list(ram.ft for ram in self._l_ramdata)
            if self._l_ramdata is not None
            else None,
            **dict_setting,
        )

        # compose metadata for the combined ramdata
        if self.is_combined:
            # %% COMBINED %%
            """write metadata"""
            if not zarr_exists(self._path_folder_ramdata):
                self._root = zarr.open(self._path_folder_ramdata, "a")
                # compose metadata
                self._dict_metadata = {
                    "path_folder_mtx_10x_input": None,
                    "str_completed_time": bk.TIME_GET_timestamp(True),
                    "int_num_features": self.ft.int_num_entries,
                    "int_num_barcodes": self.bc.int_num_entries,
                    "layers": dict(),
                    "models": dict(),
                    "version": _version_,
                    "identifier": bk.UUID(),
                }
                self.set_metadata(self._dict_metadata)  # write the metadata
        self.metadata  # load metadata

        # initialize the layor object
        if (
            name_layer is not None and name_layer in self.layers
        ):  # if given name of the layer is valid
            self.layer = name_layer

        # initialize utility databases
        if (
            self._path_folder_ramdata_local is not None
        ):  # retrieve ramdata object in the local file system, and if the object is available, load/initialize anndatacontainer and shelvecontainer in the local file system
            if flag_load_anndata_container:
                # set AnnDataContainer attribute for containing various AnnData objects associated with the current RamData
                self.ad = AnnDataContainer(
                    path_prefix_default=self._path_folder_ramdata_local,
                    flag_enforce_name_adata_with_only_valid_characters=flag_enforce_name_adata_with_only_valid_characters,
                    **bk.GLOB_Retrive_Strings_in_Wildcards(
                        f"{self._path_folder_ramdata_local}*.h5ad"
                    )
                    .set_index("wildcard_0")
                    .path.to_dict(),
                    mode=self._mode,
                    path_prefix_default_mask=self._path_folder_ramdata_mask,
                    flag_is_read_only=self._flag_is_read_only,
                )  # load locations of AnnData objects stored in the RamData directory

            # open a shelve-based persistent dictionary to save/retrieve arbitrary picklable python objects associated with the current RamData in a memory-efficient manner
            self.ns = ShelveContainer(
                f"{self._path_folder_ramdata_local}ns",
                mode=self._mode,
                path_prefix_shelve_mask=f"{self._path_folder_ramdata_mask}ns",
                flag_is_read_only=self._flag_is_read_only,
            )
        else:  # initialize anndatacontainer and shelvecontainer in the memory using a dicitonary (a fallback)
            self.ad = dict()
            self.ns = dict()

    @property
    def path_folder(self):
        """# 2023-04-12 17:19:28"""
        return self._path_folder_ramdata

    @property
    def flag_spawn(self):
        """# 2023-03-26 01:35:37
        return 'flag_spawn' attribute
        """
        return self._flag_spawn

    @property
    def obs(self):
        """# 2023-02-09 22:01:54
        scanpy-style interface
        """
        return self.bc

    @property
    def var(self):
        """# 2023-02-09 22:01:54
        scanpy-style interface
        """
        return self.ft

    @property
    def int_num_cpus(self):
        """# 2023-01-20 17:41:25
        number of cpu cores to use for RamData and RamDataAxis operations
        """
        return self._int_num_cpus

    @int_num_cpus.setter
    def int_num_cpus(self, val):
        """# 2023-01-20 17:41:25
        change the number of cpu cores to use for RamData and RamDataAxis operations
        """
        self._int_num_cpus = val
        self.bc.int_num_cpus = val
        self.ft.int_num_cpus = val

    @property
    def int_num_cpus_for_updating_metadata(self):
        """# 2023-01-20 17:41:25
        return the number of cpu cores for updating metadata
        """
        return self._int_num_cpus_for_updating_metadata

    @int_num_cpus_for_updating_metadata.setter
    def int_num_cpus_for_updating_metadata(self, val):
        """# 2023-01-20 17:41:25
        change the number of cpu cores for updating metadata
        """
        self._int_num_cpus_for_updating_metadata = val
        self.bc.m.int_num_cpus = val
        self.ft.m.int_num_cpus = val

    @property
    def locking_server(self):
        """# 2022-12-23 00:02:37
        return 'ZarrSpinLockServer' object
        """
        return self._zsls

    @locking_server.setter
    def locking_server(self, locking_server_new):
        """# 2022-12-23 00:02:43"""
        self._zsls = (
            locking_server_new  # set 'ZarrSpinLockServer' of the current object
        )
        self.bc.locking_server = (
            locking_server_new  # set 'ZarrSpinLockServer' of the 'bc' axis
        )
        self.ft.locking_server = (
            locking_server_new  # set 'ZarrSpinLockServer' of the 'ft' axis
        )

        if self.layer is not None:  # if the layer has been loaded
            self.layer.locking_server = (
                locking_server_new  # set 'ZarrSpinLockServer' of the layer
            )

    def get_fork_safe_version(self):
        """# 2022-12-22 23:35:12
        return a fork-safe version by creating a new 'ZarrSpinLockServer' object and replace the previous 'ZarrSpinLockServer'
        """
        # create a new 'ZarrSpinLockServer'
        zsls = ZarrSpinLockServer(
            flag_spawn=True,
            dict_kwargs_credentials_s3=self._dict_kwargs_credentials_s3,
            flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock=self._flag_does_not_wait_and_raise_error_when_modification_is_not_possible_due_to_lock,
            float_second_to_wait_before_checking_availability_of_a_spin_lock=self._float_second_to_wait_before_checking_availability_of_a_spin_lock,
        )

        self.locking_server = zsls
        return self

    def terminate_spawned_processes(self):
        """# 2022-12-26 08:19:57
        destroy spawned processes
        """
        if self._zsls is not None:  # if file-locking is used
            # terminate the locking server
            self._zsls.terminate()

    @property
    def identifier(self):
        """# 2022-09-23 17:26:18
        return the identifier
        """
        # [TEMP] add identifier
        if "identifier" not in self._dict_metadata:
            self.update_metadata(dict_metadata_to_be_updated={"identifier": bk.UUID()})

        return self._dict_metadata["identifier"]

    def get_component(self, int_index=None, str_identifier: Union[str, None] = None):
        """# 2022-09-23 20:10:31

        get component RamData using integer index or a string identifier
        """
        if int_index is not None and str_identifier is not None:
            if self.verbose:
                logger.info(
                    "[RamData.get_component] only one of 'int_index' or 'str_identifier' should be given but both were given, exiting"
                )
            return
        # if current RamData has a matching 'str_identifier', return 'self'
        if (
            str_identifier is not None and self.identifier == str_identifier
        ):  # if current RamData matches the query, return self
            return self

        # handle when current RamData has components
        if self.is_combined:
            # handle 'int_index' query
            if int_index is not None:
                return self._l_ramdata[int_index]

            # search through each component ramdata
            for ram in self._l_ramdata:
                ram_matched = ram.get_component(
                    str_identifier=str_identifier
                )  # check whether the current component contains RamData matching the query
                if ram_matched is not None:
                    return ram_matched

    @property
    def int_index_component_reference(self):
        """# 2022-09-22 02:35:20
        return the index of the reference component
        """
        return self._int_index_component_reference

    @int_index_component_reference.setter
    def int_index_component_reference(self, val):
        """# 2023-02-27 20:30:46
        validate and update the index of the reference component if 'combined' mode is used. if None is given, deactivate the 'reference' mode
        """
        if self.is_combined:
            if val is not None and not (
                0 <= val < self.int_num_components
            ):  # when invalid value was given, by default, use 0 as the reference ramdata
                val = 0

            if (
                val != self._int_index_component_reference
            ):  # if the reference component has been changed.
                self._int_index_component_reference = (
                    val  # set 'int_index_component_reference'
                )

                if self.verbose:  # report
                    if val is not None:  # if valid index has been given
                        logging.info(
                            f"RamData component '{val}' has been set as the reference RamData component."
                        )

                # unload the layer
                if (
                    self.layer is not None
                ):  # if a layer has been loaded, unload once the reference ramdata component has been changed.
                    self.layer = None

    @property
    def index_ramdata_source_for_combined_barcodes_shared_across_ramdata(self):
        """# 2022-09-20 15:03:26
        return 'index_ramdata_source_for_combined_barcodes_shared_across_ramdata'
        """
        return self._index_ramdata_source_for_combined_barcodes_shared_across_ramdata

    @property
    def index_ramdata_source_for_combined_features_shared_across_ramdata(self):
        """# 2022-09-20 15:03:26
        return 'index_ramdata_source_for_combined_features_shared_across_ramdata'
        """
        return self._index_ramdata_source_for_combined_features_shared_across_ramdata

    @index_ramdata_source_for_combined_barcodes_shared_across_ramdata.setter
    def index_ramdata_source_for_combined_barcodes_shared_across_ramdata(self, index):
        """# 2022-09-20 15:03:26
        return 'index_ramdata_source_for_combined_barcodes_shared_across_ramdata'
        """
        self.bc.index_ax_data_source_when_interleaved = index  # change the axis setting
        self._index_ramdata_source_for_combined_barcodes_shared_across_ramdata = index

    @index_ramdata_source_for_combined_features_shared_across_ramdata.setter
    def index_ramdata_source_for_combined_features_shared_across_ramdata(self, index):
        """# 2022-09-20 15:03:26
        return 'index_ramdata_source_for_combined_features_shared_across_ramdata'
        """
        self.ft.index_ax_data_source_when_interleaved = index  # change the axis setting
        self._index_ramdata_source_for_combined_features_shared_across_ramdata = index

    @property
    def has_mask(self):
        """# 2022-09-18 00:01:13
        return True if current RamData contains mask
        """
        return self._path_folder_ramdata_mask is not None

    @property
    def is_component(self):
        """# 2022-09-03 15:35:38
        return True if the current RamData is a component of a RamData
        """
        return self._ramdata_composite is not None

    @property
    def is_combined(self):
        """# 2022-08-29 15:29:10
        return True if current RamData is in 'combined' mode
        """
        return self._l_ramdata is not None

    @property
    def int_num_components(self):
        """# 2022-09-16 02:47:13
        return the number of component RamData objects
        """
        int_num_components = len(self._l_ramdata) if self.is_combined else None
        return int_num_components

    @property
    def int_num_cpus_for_fetching_data(self):
        """# 2022-07-21 23:32:24"""
        return self._int_num_cpus_for_fetching_data

    @int_num_cpus_for_fetching_data.setter
    def int_num_cpus_for_fetching_data(self, val):
        """# 2022-07-21 23:32:35"""
        self._int_num_cpus_for_fetching_data = max(1, int(val))  # set an integer value
        if self.layer is not None:
            self.layer.int_num_cpus = (
                self._int_num_cpus_for_fetching_data
            )  # update 'int_num_cpus' attributes of RAMtxs

    """ <Methods for handling Paths> """

    @property
    def is_remote(self):
        """# 2022-09-03 17:17:32
        return True if the RamData is located remotely
        """
        return is_remote_url(self._path_folder_ramdata)

    @property
    def contains_remote(self):
        """# 2022-09-05 17:55:26
        return True if current RamData is in remote location or contains component RamData hosted remotely
        """
        # if current ramdata is in remote location, return True
        if self.is_remote:
            return True
        # if current ramdata is in combined mode, survey its component and identify ramdata located remotely
        if self.is_combined:
            for ram in self._l_ramdata:
                if ram is not None and ram.is_remote:
                    return True

    @property
    def _path_folder_ramdata_modifiable(self):
        """# 2022-07-21 00:07:23
        return path of the ramdata that is modifiable based on the current RamData settings.
        if mask is given, path to the mask will be returned.
        if current ramdata location cannot be modified and no mask has been given, None will be returned.
        """
        if self._path_folder_ramdata_mask is not None and not is_remote_url(
            self._path_folder_ramdata_mask
        ):  # if mask is given and is located locally, use the mask (it is unlikely that Amazon S3 object is used as a mask)
            return self._path_folder_ramdata_mask
        elif (
            not self._flag_is_read_only
        ):  # if current object can be modified, create temp folder inside the current object
            return self._path_folder_ramdata
        else:
            return None

    @property
    def _path_folder_ramdata_local(self):
        """# 2022-07-21 02:08:55
        return path of the ramdata that is in the local file system based on the current RamData settings.
        if mask is given, path to the mask will be returned, since mask is assumed to be present in the local file system.
        """
        if (
            self._path_folder_ramdata_mask is not None
        ):  # if mask is given, use the mask, since mask is assumed to be present in the local file system.
            return self._path_folder_ramdata_mask
        elif (
            "://" not in self._path_folder_ramdata
        ):  # if current object appears to be in the local file system, use the current object
            return self._path_folder_ramdata
        else:
            return None

    @property
    def _path_folder_ramdata_active(self):
        """# 2022-12-13 21:31:51
        return path of the ramdata that is currently active in the current object.
        if mask is present, path to the mask will be given.
        """
        if (
            self._path_folder_ramdata_mask is not None
        ):  # if mask is given, use the mask, since mask is assumed to be present in the local file system.
            return self._path_folder_ramdata_mask
        else:
            return self._path_folder_ramdata

    @property
    def path_folder_temp(self):
        """# 2022-12-06 23:41:31
        return the path to the temporary folder (a read-only attribute)
        """
        return self._path_folder_temp

    """ </Methods for handling Paths> """
    """ <Methods for Synchronization> """

    @property
    def use_locking(self):
        """# 2022-12-12 02:45:43
        return True if a spin lock algorithm is being used for synchronization of operations on the current object
        """
        return self._zsls is not None

    @property
    def metadata(self):
        """# 2022-07-21 02:38:31"""
        return self.get_metadata()

    def get_metadata(self):
        """# 2022-12-13 02:00:26
        read metadata with file-locking (also implement lazy-loading of metadata)
        """
        if not hasattr(self, "_root"):  # initialize the zarr group
            # open RamData as a Zarr object (group)
            self._root = zarr.open(self._path_folder_ramdata)
            if (
                self._path_folder_ramdata_mask is not None
            ):  # if mask is given, open the mask object as a zarr group to save/retrieve metadata
                root_mask = zarr.open(
                    self._path_folder_ramdata_mask
                )  # open the mask object as a zarr group
                if (
                    len(list(root_mask.attrs)) == 0
                ):  # if mask object does not have a ramdata attribute
                    if self.use_locking:  # %% FILE LOCKING %%
                        self._zsls.wait_lock(
                            f"{self._path_folder_ramdata}.zattrs.lock/"
                        )  # wait until a lock is released before reading the metadata of the current RamData object
                    root_mask.attrs["dict_metadata"] = self._root.attrs[
                        "dict_metadata"
                    ]  # copy the ramdata attribute of the current RamData to the mask object
                self._root = root_mask  # use the mask object zarr group to save/retrieve ramdata metadata

        path_folder = (
            self._path_folder_ramdata_active
        )  # retrieve path to the active ramdata object
        if (
            self.use_locking
        ):  # when locking has been enabled, read metadata from the storage, and update the metadata currently loaded in the memory
            # %% FILE LOCKING %%
            self._zsls.wait_lock(
                f"{path_folder}.zattrs.lock/"
            )  # wait until a lock is released
            self._dict_metadata = self._zsls.zms.get_metadata(
                path_folder, "dict_metadata"
            )  # retrieve metadata from the storage, and update the metadata stored in the object

        #             # 🐘TEMP(for converting temporary metadata structures)🐘
        #             # update 'layers' metadata structure
        #             if not isinstance( self._dict_metadata[ 'layers' ], dict ) :
        #                 self._dict_metadata[ 'layers' ] = dict( ( e, dict( ) ) for e in self._dict_metadata[ 'layers' ] )

        #             # create the model metadata
        #             if 'models' not in self._dict_metadata :
        #                 self._dict_metadata[ 'models' ] = dict( )

        #             # update 'models' metadata structure
        #             if 'ipca' in self._dict_metadata[ 'models' ] :
        #                 dict_models = dict( )
        #                 for type_model in self._dict_metadata[ 'models' ] :
        #                     for name_model in self._dict_metadata[ 'models' ][ type_model ] :
        #                         id_model = f"{name_model}|{type_model.lower( )}" # compose 'id_model' that identifies the model
        #                         dict_models[ id_model ] = { 'file_size_in_bytes' : self._dict_metadata[ 'models' ][ type_model ][ name_model ] }
        #                     self._dict_metadata[ 'models' ]
        #                 self._dict_metadata[ 'models' ] = dict_models

        #             # save metadata
        #             self.set_metadata( self._dict_metadata )
        elif not hasattr(
            self, "_dict_metadata"
        ):  # when locking is not used but the metadata has not been loaded, read the metadata without using the locking algorithm
            self._dict_metadata = self._root.attrs[
                "dict_metadata"
            ]  # retrieve 'dict_metadata' from the storage
        return self._dict_metadata  # return the metadata

    def set_metadata(self, dict_metadata: dict):
        """# 2022-12-11 22:08:05
        write metadata with file-locking
        """
        path_folder = (
            self._path_folder_ramdata_active
        )  # retrieve path to the active ramdata object
        if (
            self._flag_is_read_only
        ):  # save metadata only when it is not in the read-only mode
            return
        self._dict_metadata = dict_metadata  # update metadata stored in the memory
        if (
            self._zsls is None
        ):  # if locking is not used, return previously loaded metadata
            self._root.attrs["dict_metadata"] = self._dict_metadata
        else:  # when locking has been enabled
            self._zsls.acquire_lock(f"{path_folder}.zattrs.lock/")  # acquire a lock
            self._zsls.zms.set_metadata(
                path_folder, "dict_metadata", self._dict_metadata
            )  # write metadata to the storage
            self._zsls.release_lock(f"{path_folder}.zattrs.lock/")  # release the lock

    def update_metadata(
        self,
        dict_metadata_to_be_updated: dict = dict(),
        l_name_layer_to_be_deleted: list = [],
        dict_rename_name_layer: dict = dict(),
        l_id_model_to_be_deleted: list = [],
        dict_rename_id_model: dict = dict(),
    ):
        """# 2022-12-14 11:24:50
        write metadata with file-locking

        dict_metadata_to_be_updated : dict # a dictionarty for updating 'dict_metadata' of the current object
        l_name_layer_to_be_deleted : list = [ ] # a list of name of layers to be deleted from the metadata.
        dict_rename_name_layer : dict = dict( ) # a dictionary mapping previous name_layer to new name_layer for renaming layers
        l_id_model_to_be_deleted : list = [ ] # a list of id_models to be deleted
        dict_rename_id_model : dict = dict( ) # a dictionary mapping previous id_model to new id_model for renaming models
        """
        if (
            self._flag_is_read_only
        ):  # update the metadata only when it is not in the read-only mode
            return
        path_folder = (
            self._path_folder_ramdata_active
        )  # retrieve path to the active ramdata object

        def __update_dict_metadata(
            dict_metadata: dict,
            dict_metadata_to_be_updated: dict,
            l_name_layer_to_be_deleted: list,
            dict_rename_name_layer: dict,
            l_id_model_to_be_deleted: list,
            dict_rename_id_model: dict,
        ):
            """# 2022-12-13 19:30:27
            update dict_metadata with dict_metadata_to_be_updated and return the updated dict_metadata
            """
            # update 'layer' metadata separately
            if "layers" in dict_metadata_to_be_updated:
                dict_metadata_layers = dict_metadata["layers"]
                dict_metadata_layers.update(dict_metadata_to_be_updated["layers"])
                dict_metadata_to_be_updated["layers"] = dict_metadata_layers

            # update 'models' metadata separately
            if "models" in dict_metadata_to_be_updated:
                dict_metadata_models = dict_metadata["models"]
                dict_metadata_models.update(dict_metadata_to_be_updated["models"])
                dict_metadata_to_be_updated["models"] = dict_metadata_models

            # update 'dict_metadata'
            dict_metadata.update(dict_metadata_to_be_updated)

            # delete layers from the 'dict_metadata'
            for name_layer in l_name_layer_to_be_deleted:
                if name_layer in dict_metadata["layers"]:
                    dict_metadata["layers"].pop(name_layer)

            # rename layers of the 'dict_metadata'
            for name_layer_prev in dict_rename_name_layer:
                name_layer_new = dict_rename_name_layer[name_layer_prev]
                if (
                    name_layer_prev in dict_metadata["layers"]
                    and name_layer_new not in dict_metadata["layers"]
                ):  # for a valid pair of previous and new layer names
                    dict_metadata["layers"][name_layer_new] = dict_metadata[
                        "layers"
                    ].pop(
                        name_layer_prev
                    )  # perform a renaming operation

            # delete models from the 'dict_metadata'
            for id_model in l_id_model_to_be_deleted:
                if id_model in dict_metadata["models"]:
                    dict_metadata["models"].pop(id_model)

            # rename models of the 'dict_metadata'
            for id_model_prev in dict_rename_id_model:
                id_model_new = dict_rename_id_model[id_model_prev]
                if (
                    id_model_prev in dict_metadata["models"]
                    and id_model_new not in dict_metadata["models"]
                ):  # for a valid pair of previous and new id_models
                    dict_metadata["models"][id_model_new] = dict_metadata["models"].pop(
                        id_model_prev
                    )  # perform a renaming operation

            return dict_metadata

        if (
            self._zsls is None
        ):  # if locking is not used, return previously loaded metadata
            self._dict_metadata = __update_dict_metadata(
                self._dict_metadata,
                dict_metadata_to_be_updated,
                l_name_layer_to_be_deleted,
                dict_rename_name_layer,
                l_id_model_to_be_deleted,
                dict_rename_id_model,
            )  # update 'self._dict_metadata' with 'dict_metadata_to_be_updated'
            self._root.attrs["dict_metadata"] = self._dict_metadata
        else:  # when locking has been enabled
            self._zsls.acquire_lock(f"{path_folder}.zattrs.lock/")  # acquire a lock

            self._dict_metadata = self._zsls.zms.get_metadata(
                path_folder, "dict_metadata"
            )  # read metadata from the storage and update the metadata
            self._dict_metadata = __update_dict_metadata(
                self._dict_metadata,
                dict_metadata_to_be_updated,
                l_name_layer_to_be_deleted,
                dict_rename_name_layer,
                l_id_model_to_be_deleted,
                dict_rename_id_model,
            )  # update 'self._dict_metadata' with 'dict_metadata_to_be_updated'
            self._zsls.zms.set_metadata(
                path_folder, "dict_metadata", self._dict_metadata
            )  # write metadata to the storage

            self._zsls.release_lock(f"{path_folder}.zattrs.lock/")  # release the lock

    def _add_layer(self, name_layer: str, dict_metadata_description: dict = dict()):
        """# 2022-11-15 00:14:14
        a semi-private method for adding a layer to the current RamData

        dict_metadata_description : dict = dict( ) # 'dict_metadata_description' of the layer.
        """
        if (
            name_layer not in self.layers_excluding_components
        ):  # if the layer is not present in the current object
            self.update_metadata(
                dict_metadata_to_be_updated={
                    "layers": {name_layer: dict_metadata_description}
                }
            )

    def _save_metadata_(self):
        """# 2022-12-13 19:49:45
        save metadata of the current ZarrDataFrame
        """
        if (
            not self._flag_is_read_only
        ):  # save metadata only when it is not in the read-only mode
            if hasattr(self, "_dict_metadata"):  # if metadata has been loaded
                self.set_metadata(
                    dict_metadata=self._dict_metadata
                )  # update the metadata

    """ functions for multiprocessing """

    def initialize_workers(self):
        """# 2023-03-08 21:47:00
        initialize workers
        """
        if not hasattr(
            self, "flag_workers_initialized"
        ):  # initialize workers only once
            context = None  # initialize the context
            if self.is_remote:
                context = mp.get_context("spawn")

            self.executor = concurrent.futures.ProcessPoolExecutor(
                mp_context=context
            )  # retrieve executor
            self.flag_workers_initialized = (
                True  # set the flag indicating workers have been implemented.
            )

    """ utility functions for saving/loading models """

    @property
    def models(self):
        """# 2022-09-03 19:13:40
        show available models of the RamData, including models in the components and mask
        """
        models = deepcopy(self._dict_metadata["models"])  # create a copy
        if self.is_combined:
            # %% COMBINED %%
            for ram in self._l_ramdata:
                for id_model in ram.models:
                    if (
                        id_model not in models
                    ):  # update 'id_model' only when the current 'id_model' does not exist in the models metadata
                        models[id_model] = ram.models[id_model]
        return models

    @property
    def models_excluding_components(self):
        """# 2022-09-03 19:13:34
        show available models of the RamData excluding models from the RamData components.
        """
        models = deepcopy(self._dict_metadata["models"])  # create a copy
        return models

    def get_model_prefix(
        self,
        name_model: str,
        type_model: Literal[
            "ipca",
            "pumap",
            "hdbscan",
            "knn_classifier",
            "knn_embedder",
            "knngraph",
            "knnindex",
            "deep_learning.keras.classifier",
            "deep_learning.keras.embedder",
        ],
    ):
        """ # 2023-05-06 07:06:35 
        get a prefix of the file name of the model.
        replaces characters incompatible with the file system with escape characters
        """
        return get_path_compatible_str( 
            str_input = name_model,
            str_invalid_char = "<>:/\|?*" + '"', # reserved characters in Windows file system
            int_max_num_bytes_in_a_folder_name = 255 - len( type_model ) - 1 - 7, # the maximum number of bytes for a folder name in Linux (255) # additional number of bytes (8) required for certain operations of the RamData
        ) + f'.{type_model}'
    
    def get_model_path(
        self,
        name_model: str,
        type_model: Literal[
            "ipca",
            "pumap",
            "hdbscan",
            "knn_classifier",
            "knn_embedder",
            "knngraph",
            "knnindex",
            "deep_learning.keras.classifier",
            "deep_learning.keras.embedder",
        ],
        index_component: Union[int, None] = None,
    ):
        """# 2022-09-17 00:34:50
        get a valid path of the model (either remote or local) recursively from mask and components

        name_model : str # the name of the model
        type_model : Literal[ 'ipca', 'pumap', 'hdbscan', 'knn_classifier', 'knn_embedder', 'knngraph', 'knnindex' ] # the type of model
        index_component : Union[ int, None ] = None # the index of the RamData component from which to retrieve models
        """
        if not self.check_model(
            name_model, type_model, flag_exclude_components=False
        ):  # if the model does not exist in the current ramdata, return None
            return None

        # handle inputs
        if self.is_combined and index_component is not None:
            if not (
                0 <= index_component < self.int_num_components
            ):  # if invalid 'int_num_components' was given, set default value (0)
                index_component = 0

        # define internal functions
        def __get_name_file_of_a_model(name_model, type_model):
            """# 2022-09-17 23:57:45
            get name of the file of a given model
            """
            str_prefix_file_model = self.get_model_prefix( name_model, type_model ) # retrieve the prefix of the file
            
            if type_model in self._set_type_model_picklable:  # handle picklable models
                name_file_model = f"{str_prefix_file_model}.pickle"
            else:  # other models will be tar-gzipped
                name_file_model = f"{str_prefix_file_model}.tar.gz"
            return name_file_model

        def __check_file_exists(path_file):
            """# 2022-09-17 23:18:13
            check whether the model file exists in the given ramdata
            'flag_modifiable' : set this to True for checking whether a file exists in the modifiable path
            """
            if is_remote_url(path_file):
                if is_s3_url(path_file):
                    return s3_exists(path_file)  # check whether s3 file exists
                elif is_http_url(path_file):
                    return (
                        http_response_code(path_file) == 200
                    )  # check whether http file exists
            else:
                return filesystem_operations(
                    "exists", path_file
                )  # check whether the file exists in the local file system

        path_file = None  # initialize the output value
        name_model_file = __get_name_file_of_a_model(
            name_model, type_model
        )  # get the name of the file containing the model

        if self.check_model(
            name_model, type_model, flag_exclude_components=True
        ):  # if the model does not exist in the component, file path from mask and current RamData
            # check whether the model exists in the current RamData
            _path_file = f"{self._path_folder_ramdata}models/{name_model_file}"
            if __check_file_exists(_path_file):
                path_file = _path_file

            # if the current RamData has mask, check whether the model exists in the mask
            if self.has_mask:
                _path_file = f"{self._path_folder_ramdata_mask}models/{name_model_file}"
                if __check_file_exists(_path_file):
                    path_file = _path_file  # overwrite the path of the model exists in the original RamData
        else:
            if self.is_combined:
                # %% COMBINED %%
                if (
                    index_component is not None
                ):  # if valid integer index of the target component has been given
                    path_file = self._l_ramdata[index_component].get_model_path(
                        name_model, type_model
                    )  # retrieve model path from the
                else:
                    for ram in self._l_ramdata:  # iterate over component
                        path_file = ram.get_model_path(name_model, type_model)
                        if (
                            path_file is not None
                        ):  # exit once a valid model path has been retrieved
                            break
        return path_file  # return the path of the identified model

    def check_model(
        self,
        name_model: str,
        type_model: Literal[
            "ipca",
            "pumap",
            "hdbscan",
            "knn_classifier",
            "knn_embedder",
            "knngraph",
            "knnindex",
            "deep_learning.keras.classifier",
            "deep_learning.keras.embedder",
        ],
        flag_exclude_components: bool = False,
    ):
        """# 2022-12-14 12:31:59

        return True if the model exists in the current RamData, and return False if the model does not exist in the current RamData

        flag_exclude_components : bool = False # the exclude models that only exist in RamData components
        """
        models = (
            self.models_excluding_components if flag_exclude_components else self.models
        )  # retrieve currently available models
        return (
            f"{name_model}|{type_model}" in models
        )  # return True if the id_model exists in the models

    def load_model(
        self,
        name_model: str,
        type_model: Literal[
            "ipca",
            "pumap",
            "hdbscan",
            "knn_classifier",
            "knn_embedder",
            "knngraph",
            "knnindex",
            "deep_learning.keras.classifier",
            "deep_learning.keras.embedder",
        ],
        index_component: Union[int, None] = None,
    ):
        """# 2023-05-06 17:57:01 
        load model from the current RamData.

        name_model : str # the name of the model
        type_model : Literal[ 'ipca', 'pumap', 'hdbscan', 'knn_classifier', 'knn_embedder', 'knngraph', 'knnindex' ] # the type of model
        index_component : Union[ int, None ] = None # the index of the RamData component from which to retrieve models
        """
        if not self.check_model(
            name_model, type_model, flag_exclude_components=False
        ):  # if the model does not exist in the current ramdata, return None
            return None
        
        str_prefix_file_model = self.get_model_prefix( name_model, type_model ) # retrieve the prefix of the file 

        # handle inputs
        if self.is_combined:
            if index_component is not None:
                if not (
                    0 <= index_component < self.int_num_components
                ):  # if invalid 'int_num_components' was given, set default value (0)
                    index_component = 0
            else:
                index_component = (
                    self.int_index_component_reference
                )  # by default, use 'self.int_index_component_reference' as the index of the reference component

        # load model only when modifiable ramdata exists (the model should be present in the local storage and should be in the 'modifiable' directory)
        if self._path_folder_ramdata_modifiable is None:
            return

        # define a folder for storage of models
        path_folder_models = f"{self._path_folder_ramdata_modifiable}models/"  # define a folder to save/load model
        filesystem_operations("mkdir", path_folder_models, exist_ok=True)

        # define internal functions
        def __search_and_download_model_file(name_model_file):
            """# 2022-12-02 19:09:39
            check availability of models and download model file from the remote location where RamData is being hosted.
            """
            # define the paths of the model files
            path_file_dest = f"{path_folder_models}{name_model_file}"  # local path
            if filesystem_operations(
                "exists", path_file_dest
            ):  # check whether the destination file already exists
                return

            path_file_src = self.get_model_path(
                name_model, type_model, index_component=index_component
            )
            if path_file_src is None:  # if source file is not available
                return False

            # file-locking (simply checking the presense of the lock)
            if self.use_locking:  # %% FILE LOCKING %%
                path_folder_model_src = f"{path_file_src.rsplit( '/', 1 )[ 0 ]}/"  # retrieve the folder path of the models of the source RamData
                self._zsls.wait_lock(
                    f"{path_folder_model_src}{str_prefix_file_model}.lock/"
                )

            if is_remote_url(path_file_src):
                if is_s3_url(path_file_src):
                    s3_download_file(
                        path_file_src, path_file_dest
                    )  # download file from s3 object
                elif is_http_url(path_file_src):
                    http_download_file(
                        path_file_src, path_file_dest
                    )  # download file using HTTP
            else:  # if the source file is available locally
                filesystem_operations(
                    "cp", path_file_src, path_file_dest
                )  # or copy file

        # load model
        if type_model in self._set_type_model_picklable:  # handle picklable models
            # define path
            name_model_file = f"{str_prefix_file_model}.pickle"
            path_file_model = f"{path_folder_models}{name_model_file}"

            # download the model file
            __search_and_download_model_file(name_model_file)

            # exit if the file does not exists
            if not filesystem_operations("exists", path_file_model):
                return

            model = bk.PICKLE_Read(path_file_model)
        elif type_model == "pumap":  # parametric umap model
            import umap.parametric_umap as pumap  # parametric UMAP

            # define paths
            name_model_file = f"{str_prefix_file_model}.tar.gz"
            path_prefix_model = f"{path_folder_models}{str_prefix_file_model}"
            path_file_model = path_prefix_model + ".tar.gz"

            # download the model file
            __search_and_download_model_file(name_model_file)

            # exit if the file does not exists
            if not filesystem_operations("exists", path_file_model):
                return

            # extract tar.gz
            if not filesystem_operations(
                "exists", path_prefix_model
            ):  # if the model has not been extracted from the tar.gz archive
                tar_extract(
                    path_file_model, path_folder_models
                )  # extract tar.gz file of pumap object
            model = pumap.load_ParametricUMAP(path_prefix_model)  # load pumap model

            # fix 'load_ParametricUMAP' error ('decoder' attribute does not exist)
            if not hasattr(model, "decoder"):
                model.decoder = None
        elif (
            type_model in self._set_type_model_keras_model
        ):  # handle 'dict_model' containing 'dl_model'
            import tensorflow as tf

            # define paths
            name_model_file = f"{str_prefix_file_model}.tar.gz"
            path_prefix_model = f"{path_folder_models}{str_prefix_file_model}"
            path_file_model = path_prefix_model + ".tar.gz"

            # download the model file
            __search_and_download_model_file(name_model_file)

            # exit if the file does not exists
            if not filesystem_operations("exists", path_file_model):
                return

            # extract tar.gz
            if not filesystem_operations(
                "exists", path_prefix_model
            ):  # if the model has not been extracted from the tar.gz archive
                tar_extract(
                    path_file_model, path_folder_models
                )  # extract tar.gz file of pumap object

            model = bk.PICKLE_Read(
                f"{path_prefix_model}/metadata.pickle"
            )  # load metadata first
            model["dl_model"] = tf.keras.models.load_model(
                f"{path_prefix_model}/dl_model.hdf5"
            )  # load keras model
        return model  # return loaded model

    def save_model(
        self,
        model,
        name_model: str,
        type_model: Literal[
            "ipca",
            "pumap",
            "hdbscan",
            "knn_classifier",
            "knn_embedder",
            "knngraph",
            "knnindex",
            "deep_learning.keras.classifier",
            "deep_learning.keras.embedder",
        ],
        dict_metadata_description: dict = dict(),
    ):
        """# 2023-05-06 17:51:32 
        save model to RamData. if mask is available, save model to the mask

        'model' : input model
        'name_model' : the name of the model. if the same type of model with the same model name already exists, it will be overwritten
        'type_model' : the type of models. currently [ 'ipca', 'pumap' ], for PCA transformation and UMAP embedding, are supported
        dict_metadata_description : dict = dict( ) # 'dict_metadata_description' of the model.
        """
        # save model only when mode != 'r'
        if self._mode == "r":
            return
        # save model only when modifiable ramdata exists
        if self._path_folder_ramdata_modifiable is None:
            return

        # define a folder for storage of models
        path_folder_models = f"{self._path_folder_ramdata_modifiable}models/"  # define a folder to save/load model
        filesystem_operations("mkdir", path_folder_models, exist_ok=True)

        # retrieve the prefix of the file
        str_prefix_file_model = self.get_model_prefix( name_model, type_model ) 
        
        try:
            # locking
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.acquire_lock(
                    f"{path_folder_models}{str_prefix_file_model}.lock/"
                )
            # use temporary folder when the destination folder is located remotely
            path_folder_models_local = (
                path_folder_models  # set default 'path_folder_models_local'
            )
            if is_remote_url(
                self._path_folder_ramdata_modifiable
            ):  # when the destination folder is located remotely, the temporary local folder should be used.
                path_folder_models_local = f"{self._path_folder_temp}models/"  # define a local folder to save/load model
                filesystem_operations(
                    "mkdir", path_folder_models_local
                )  # create a local folder

            # if the model already exists in the current RamData (excluding components), delete the model
            if self.check_model(
                name_model=name_model,
                type_model=type_model,
                flag_exclude_components=True,
            ):  # exclude components
                self.delete_model(name_model=name_model, type_model=type_model)

            # save model (assume 'path_folder_models_local' is located in the local storage)
            if type_model in self._set_type_model_picklable:  # handle picklable models
                path_file_model = (
                    f"{path_folder_models_local}{str_prefix_file_model}.pickle"
                )
                bk.PICKLE_Write(path_file_model, model)
            elif type_model == "pumap":  # parametric umap model
                path_prefix_model = f"{path_folder_models_local}{name_model}.pumap"
                path_file_model = path_prefix_model + ".tar.gz"
                model.save(path_prefix_model)
                tar_create(
                    path_file_model, path_prefix_model
                )  # create tar.gz file of pumap object for efficient retrieval and download
            elif (
                type_model in self._set_type_model_keras_model
            ):  # handle 'dict_model' containing 'dl_model'
                path_prefix_model = (
                    f"{path_folder_models_local}{str_prefix_file_model}"
                )
                path_file_model = path_prefix_model + ".tar.gz"
                dl_model = model.pop(
                    "dl_model"
                )  # remove the keras model 'dl_model' from dict_model, enable the remaining 'dict_model' to become picklable
                dl_model.save(f"{path_prefix_model}/dl_model.hdf5")  # save keras model
                bk.PICKLE_Write(
                    f"{path_prefix_model}/metadata.pickle", model
                )  # save metadata as a pickle file
                tar_create(
                    path_file_model, path_prefix_model
                )  # create tar.gz file of pumap object for efficient retrieval and download
            int_file_size = os.path.getsize(
                path_file_model
            )  # retrieve file size of the saved model

            # if a temporary location was used for saving models (for remote RamData), upload the model to the remote location
            if path_folder_models_local != path_folder_models:
                filesystem_operations(
                    "cp",
                    path_file_model,
                    path_file_model.replace(
                        path_folder_models_local, path_folder_models
                    ),
                )  # upload the model
                filesystem_operations("rm", path_file_model)  # delete the local copy
        finally:
            # locking
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.release_lock(
                    f"{path_folder_models}{str_prefix_file_model}.lock/"
                )

        # update the metadata
        dict_metadata_description["file_size_in_bytes"] = int_file_size
        dict_metadata_description[
            "identifier_of_the_ramdata_of_origin"
        ] = self.identifier  # record the ramdata of origin
        self.update_metadata(
            dict_metadata_to_be_updated={
                "models": {f"{name_model}|{type_model}": dict_metadata_description}
            }
        )

        # report result
        if self.verbose:
            logger.info(f"{name_model}|{type_model} model saved.")
        return int_file_size  # return the number of bytes written

    def delete_model(
        self,
        name_model: str,
        type_model: Literal[
            "ipca",
            "pumap",
            "hdbscan",
            "knn_classifier",
            "knn_embedder",
            "knngraph",
            "knnindex",
            "deep_learning.keras.classifier",
            "deep_learning.keras.embedder",
        ],
    ):
        """# 2023-05-06 11:30:38 
        delete model of the RamData if the model exists in the RamData

        'name_model' : the name of the model. if the same type of model with the same model name already exists, it will be overwritten
        'type_model' : the type of models.
        """
        # save model only when mode != 'r'
        if self._mode == "r":
            return
        # save model only when modifiable ramdata exists
        if self._path_folder_ramdata_modifiable is None:
            return

        # if the model does not exist in the current RamData, exit
        if not self.check_model(
            name_model=name_model, type_model=type_model, flag_exclude_components=True
        ):
            return

        # define a folder for storage of models
        path_folder_models = f"{self._path_folder_ramdata_modifiable}models/"  # define a folder to save/load model
        filesystem_operations("mkdir", path_folder_models, exist_ok=True)
        
        # retrieve the prefix of the file
        str_prefix_file_model = self.get_model_prefix( name_model, type_model ) 

        try:
            # locking
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.acquire_lock(
                    f"{path_folder_models}{str_prefix_file_model}.lock/"
                )

            # delete model
            if type_model in self._set_type_model_picklable:  # handle picklable models
                path_file_model = (
                    f"{path_folder_models}{str_prefix_file_model}.pickle"
                )
            else:
                path_prefix_model = f"{path_folder_models}{str_prefix_file_model}"
                path_file_model = path_prefix_model + ".tar.gz"
                # if an extracted folder exists, delete the folder
                if filesystem_operations("exists", path_prefix_model):
                    filesystem_operations("rm", path_prefix_model)
            int_file_size = os.path.getsize(
                path_file_model
            )  # retrieve file size of the model
            filesystem_operations("rm", path_file_model)
        finally:
            # locking
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.release_lock(
                    f"{path_folder_models}{str_prefix_file_model}.lock/"
                )

        # update the metadata
        self.update_metadata(l_id_model_to_be_deleted=[f"{name_model}|{type_model}"])

        # report result
        if self.verbose:
            logger.info(f"{name_model}|{type_model} model deleted.")
        return int_file_size  # return the number of bytes of the deleted model file

    def rename_model(
        self,
        name_model: str,
        type_model: Literal[
            "ipca",
            "pumap",
            "hdbscan",
            "knn_classifier",
            "knn_embedder",
            "knngraph",
            "knnindex",
            "deep_learning.keras.classifier",
            "deep_learning.keras.embedder",
        ],
        name_model_new: str,
        flag_allow_copying: bool = False,
    ):
        """# 2023-05-06 11:33:46 
        rename a model

        name_layer_current : str # the name of the previous layer
        type_model : the type of the model
        name_layer_new : str # the name of the new layer
        flag_allow_copying : bool = False # for some storage systems, folder and directory cannot be renamed, and an entire folder should be copied and deleted in order to 'change' a folder name. in order to allow copying of an entire folder for renaming operations, set this flag to True
        """
        # save model only when mode != 'r'
        if self._mode == "r":
            return
        # save model only when modifiable ramdata exists
        if self._path_folder_ramdata_modifiable is None:
            return

        # check validity of inputs
        # if the model does not exist in the current RamData, exit
        if not self.check_model(
            name_model=name_model, type_model=type_model, flag_exclude_components=True
        ):
            logger.error(
                f"'name_model' {name_model} does not exist in the current RamData object (excluding components), exiting"
            )
            return

        # if the model does not exist in the current RamData, exit
        if self.check_model(
            name_model=name_model_new,
            type_model=type_model,
            flag_exclude_components=True,
        ):
            logger.error(
                f"the new 'name_model' {name_model_new} already exists in the current RamData object (excluding components), exiting"
            )
            return

        # rename layer # handle exceptions
        if is_s3_url(self._path_folder_ramdata_modifiable):
            logger.warning(
                "the modifiable storage location of the current RamData is Amazon S3, which does not support file renaming. renaming a file in Amazon S3 involves copying and deleting of an entire file."
            )
            if not flag_allow_copying:
                return

        # define a folder for storage of models
        path_folder_models = f"{self._path_folder_ramdata_modifiable}models/"  # define a folder to save/load model
        
        str_prefix_file_model = self.get_model_prefix( name_model, type_model ) # retrieve the prefix of the file
        str_prefix_file_model_new = self.get_model_prefix( name_model_new, type_model ) # retrieve the prefix of the new file

        try:
            # locking
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.acquire_lock(
                    f"{path_folder_models}{str_prefix_file_model}.lock/"
                )
                self._zsls.acquire_lock(
                    f"{path_folder_models}{str_prefix_file_model_new}.lock/"
                )

            # rename a model
            if type_model in self._set_type_model_picklable:  # handle picklable models
                path_file_model = (
                    f"{path_folder_models}{str_prefix_file_model}.pickle"
                )
                path_file_model_new = (
                    f"{path_folder_models}{str_prefix_file_model_new}.pickle"
                )
            else:
                path_prefix_model = f"{path_folder_models}{str_prefix_file_model}"
                path_prefix_model_new = (
                    f"{path_folder_models}{str_prefix_file_model_new}"
                )
                path_file_model = path_prefix_model + ".tar.gz"
                path_file_model_new = path_prefix_model_new + ".tar.gz"
                # if an extracted folder exists, rename the folder
                if filesystem_operations("exists", path_prefix_model):
                    filesystem_operations(
                        "mv", path_prefix_model, path_prefix_model_new
                    )
            filesystem_operations("mv", path_file_model, path_file_model_new)
        finally:
            # locking
            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.release_lock(
                    f"{path_folder_models}{str_prefix_file_model}.lock/"
                )
                self._zsls.release_lock(
                    f"{path_folder_models}{str_prefix_file_model_new}.lock/"
                )

        # update metadata (rename the id_model)
        self.update_metadata(
            dict_rename_id_model={
                f"{name_model}|{type_model}": f"{name_model_new}|{type_model}"
            }
        )

        # report result
        if self.verbose:
            logger.info(
                f"{name_model}|{type_model} model was rename to {name_model_new}|{type_model}"
            )
            
    def search_models( self, * args, ** kwargs ) :
        """# 2023-03-05 19:14:17
        search models of the current RamData object
        """
        return bk.Search_list_of_strings_with_multiple_query(
            list(self.models), *args, **kwargs
        )

    """ utility functions for columns """

    def acquire_locks_for_metadata_columns(
        self,
        axis: Union[int, str],
        l_name_col: list = [],
        flag_exclude_components: bool = True,
    ):
        """# 2022-12-14 19:22:45
        acquire locks for the given metadata columns, and return a function for releasing the locks for the given metadata columns

        === input arguments ===
        axis : Union[ int, str ]
               # 0, 'b', 'bc', 'barcode' or 'barcodes' for applying a given summarizing function for barcodes
               # 1, 'f', 'ft', 'feature' or 'features' for applying a given summarizing function for features

        l_name_col : list = [ ] # list of input columns
        flag_exclude_components : bool = True # exclude columns present in the component RamData objects. set this flag to True if columns in the component RamData objects should not be modified.

        === returns ===
        return a function for releasing the locks for the given metadata columns

        """
        if not self.use_locking:  # if locking is disabled, return None
            return
        # handle inputs
        flag_is_barcode_axis = self._determine_axis(
            axis
        )  # retrieve a flag indicating whether the data is summarized for each barcode or not
        ax = self.bc if flag_is_barcode_axis else self.ft  # retrieve the axis

        # locks of the output columns
        set_path_lock = (
            set()
        )  # initialize a set for collecting 'path_lock' of the acquired locks
        for name_col in l_name_col:
            if name_col not in ax.columns:  # skip if the name_col does not exists
                continue
            path_col = ax.meta._get_column_path(
                name_col=name_col, flag_exclude_components=flag_exclude_components
            )  # exclude columns in the components, since components should be considered as 'read-only'
            path_lock = f"{path_col}.lock"
            if (
                path_lock not in self._zsls.currently_held_locks
            ):  # if the lock has not been acquired by the current object
                self._zsls.acquire_lock(
                    path_lock
                )  # acquire locks for the columns that will be created
                set_path_lock.add(
                    path_lock
                )  # add 'path_lock' to the set of acquired locks

        zsls = self._zsls

        def release_locks():
            for path_lock in set_path_lock:
                zsls.release_lock(path_lock)

        # return a function to release the acquired locks
        return release_locks

    """ </Methods for Synchronization> """
    """ <Layer Methods> """

    @property
    def layers(self):
        """# 2022-06-24 00:14:45
        return a set of available layers
        """
        layers = set(self.metadata["layers"])  # create copy
        # add layers of the components
        if self.is_combined:
            # %% COMBINED %%
            for ram in self._l_ramdata:
                layers.update(ram.layers)  # update layers
        return layers

    @property
    def layers_excluding_components(self):
        """# 2022-06-24 00:14:45
        return a set of available layers (excluding layers of the component RamData objects)
        """
        return set(self.metadata["layers"])

    def __contains__(self, x) -> bool:
        """# 2022-06-24 00:15:04
        check whether an 'name_layer' is available in the current RamData"""
        return x in self.layers

    def __iter__(self):
        """# 2022-06-24 00:15:19
        yield each 'name_layer' upon iteration"""
        return iter(self.layers)

    @property
    def layer(self):
        """# 2022-06-24 00:16:56
        retrieve the name of layer from the layer object if it has been loaded.
        """
        return (
            self._layer if hasattr(self, "_layer") else None
        )  # if no layer is set, return None

    @layer.setter
    def layer(self, name_layer):
        """# 2022-07-20 23:29:23
        change layer to the layer 'name_layer'
        """
        # if None is given as name_layer, remove the current layer from the memory
        if name_layer is None:
            # unload layer if None is given
            if hasattr(self, "_layer"):
                self._layer.terminate_spawned_processes()  # terminate spawned processes of the previous layer
                delattr(self, "_layer")
        else:
            # check 'name_layer' is valid
            if name_layer not in self.layers:
                raise KeyError(
                    f"'{name_layer}' data does not exists in the current RamData"
                )

            if (
                self.layer is None or name_layer != self.layer.name
            ):  # if no layer has been loaded or new layer name has been given, load the new layer
                # terminate spawned processes of the previous layer
                if hasattr(self, "_layer"):
                    self._layer.terminate_spawned_processes()

                # load the layer from the collection of the component RamData objects
                if name_layer not in self.layers_excluding_components:
                    # load layer from components and compose 'l_layer'
                    l_layer = []
                    for int_index_ram, ram in enumerate(self._l_ramdata):
                        if name_layer in ram.layers:
                            if self.verbose:
                                logger.info(
                                    f"loading a layer '{name_layer}' of RamData component {int_index_ram}"
                                )
                            ram.layer = name_layer
                            l_layer.append(ram.layer)
                        else:
                            l_layer.append(None)
                    # load combined layer
                    self._layer = RamDataLayer(
                        self._path_folder_ramdata,
                        name_layer,
                        l_layer=l_layer,
                        ramdata=self,
                        dtype_of_feature_and_barcode_indices=self._dtype_of_feature_and_barcode_indices,
                        dtype_of_values=self._dtype_of_values,
                        int_num_cpus=self._int_num_cpus_for_fetching_data,
                        verbose=self.verbose,
                        mode=self._mode,
                        path_folder_ramdata_mask=self._path_folder_ramdata_mask,
                        flag_is_read_only=self._flag_is_read_only,
                        zarrspinlockserver=self._zsls,
                    )
                else:  # load the layer from the combined RamData object directly
                    self._layer = RamDataLayer(
                        self._path_folder_ramdata,
                        name_layer,
                        ramdata=self,
                        dtype_of_feature_and_barcode_indices=self._dtype_of_feature_and_barcode_indices,
                        dtype_of_values=self._dtype_of_values,
                        int_num_cpus=self._int_num_cpus_for_fetching_data,
                        verbose=self.verbose,
                        mode=self._mode,
                        path_folder_ramdata_mask=self._path_folder_ramdata_mask,
                        flag_is_read_only=self._flag_is_read_only,
                        zarrspinlockserver=self._zsls,
                    )
                if self.verbose:
                    logger.info(f"'{name_layer}' layer has been loaded")

    def rename_layer(
        self,
        name_layer_current: str,
        name_layer_new: str,
        flag_allow_copying: bool = False,
    ):
        """# 2022-12-13 22:11:49
        rename a layer

        name_layer_current : str # the name of the previous layer
        name_layer_new : str # the name of the new layer
        flag_allow_copying : bool = False # for some storage systems, folder and directory cannot be renamed, and an entire folder should be copied and deleted in order to 'change' a folder name. in order to allow copying of an entire folder for renaming operations, set this flag to True
        """
        # check validity of inputs
        # check if the current layer name exists
        if name_layer_current not in self.layers_excluding_components:
            return
        # check if the new layer name already exists in the current object
        if name_layer_new in self.layers_excluding_components:
            return
        # rename layer # handle exceptions
        if is_s3_url(self._path_folder_ramdata_modifiable):
            logger.warning(
                "the modifiable storage location of the current RamData is Amazon S3, which does not support folder renaming. renaming a folder in Amazon S3 involves copying and deleting of an entire directory."
            )
            if not flag_allow_copying:
                return

        # rename layer
        if self.use_locking:  # %% FILE LOCKING %%
            # acquire locks of both names of the layer
            self._zsls.acquire_lock(
                f"{self._path_folder_ramdata_modifiable}{name_layer_current}.lock/"
            )
            self._zsls.acquire_lock(
                f"{self._path_folder_ramdata_modifiable}{name_layer_new}.lock/"
            )

        # perform a moving operation
        filesystem_operations(
            "mv",
            f"{self._path_folder_ramdata_modifiable}{name_layer_current}",
            f"{self._path_folder_ramdata_modifiable}{name_layer_new}",
        )  # rename the folder containing the a layer

        # update metadata (rename the name of the layer)
        self.update_metadata(
            dict_rename_name_layer={name_layer_current: name_layer_new}
        )

        if self.use_locking:  # %% FILE LOCKING %%
            self._zsls.release_lock(
                f"{self._path_folder_ramdata_modifiable}{name_layer_current}.lock/"
            )
            self._zsls.release_lock(
                f"{self._path_folder_ramdata_modifiable}{name_layer_new}.lock/"
            )

    def delete_layer(self, *l_name_layer):
        """# 2022-12-13 22:11:42
        delete a given list of layers from the current RamData
        """
        # ignore if current mode is read-only
        if self._mode == "r":
            return
        for name_layer in l_name_layer:  # for each name_layer
            # only the layers present in the curren RamData (excluding the layers in the components) can be deleted.
            if name_layer not in self.layers_excluding_components:
                continue

            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.acquire_lock(
                    f"{self._path_folder_ramdata}{name_layer}.lock/"
                )

            # delete an entire layer
            filesystem_operations("rm", f"{self._path_folder_ramdata}{name_layer}/")

            # remove the current layer from the metadata
            self.update_metadata(l_name_layer_to_be_deleted=[name_layer])

            if self.use_locking:  # %% FILE LOCKING %%
                self._zsls.release_lock(
                    f"{self._path_folder_ramdata}{name_layer}.lock/"
                )

    """ </Layer Methods> """

    def _determine_axis(self, axis: Union[int, str]):
        """# 2023-05-10 18:17:13 
        return a flag indicating whether the input axis represent the 'barcode' axis

        axis : Union[ int, str ]
               # 0, 'b', 'bc', 'barcode' or 'barcodes' for applying a given summarizing function for barcodes
               # 1, 'f', 'ft', 'feature' or 'features' for applying a given summarizing function for features
        """
        # check the validility of the input arguments
        if axis not in {
            0,
            "barcode",
            1,
            "feature",
            "barcodes",
            "features",
            "bc",
            "ft",
            "b",
            "f",
        }:
            if self.verbose:
                logger.error(f"invalid argument 'axis' : '{axis}' is invalid.")
                raise KeyError(f"invalid argument 'axis' : '{axis}' is invalid.")
        # handle inputs
        flag_axis_is_barcode = axis in {
            0,
            "barcode",
            "barcodes",
            "bc",
            "b",
        }  # retrieve a flag indicating whether the axis is barcode or not
        return flag_axis_is_barcode

    def __repr__(self):
        """# 2022-07-20 00:38:24
        display RamData
        """
        return (
            f"<{'' if not self._mode == 'r' else '(read-only) '}RamData object ({'' if self.bc.filter is None else f'{self.bc.meta.n_rows}/'}{self.metadata[ 'int_num_barcodes' ]} barcodes X {'' if self.ft.filter is None else f'{self.ft.meta.n_rows}/'}{self.metadata[ 'int_num_features' ]} features"
            + (
                ""
                if self.layer is None
                else f", {self.layer.int_num_records} records in the currently active layer '{self.layer.name}'"
            )
            + f") stored at {self._path_folder_ramdata}{'' if self._path_folder_ramdata_mask is None else f' with local mask available at {self._path_folder_ramdata_mask}'}\n\twith the following layers : {self.layers}\n\t\tcurrent layer is '{self.layer.name if self.layer is not None else None}'>"
        )  # show the number of records of the current layer if available.

    def _repr_html_(self, index_component=None):
        """# 2023-02-23 22:16:42
        display RamData in an interactive environment

        'index_component' : an integer indices of the component RamData
        """
        (
            f"<{'' if not self._mode == 'r' else '(read-only) '}RamData object ({'' if self.bc.filter is None else f'{self.bc.meta.n_rows}/'}{self.metadata[ 'int_num_barcodes' ]} barcodes X {'' if self.ft.filter is None else f'{self.ft.meta.n_rows}/'}{self.metadata[ 'int_num_features' ]} features"
            + (
                ""
                if self.layer is None
                else f", {self.layer.int_num_records} records in the currently active layer '{self.layer.name}'"
            )
            + f") stored at {self._path_folder_ramdata}{'' if self._path_folder_ramdata_mask is None else f' with local mask available at {self._path_folder_ramdata_mask}'}\n\twith the following layers : {self.layers}\n\t\tcurrent layer is '{self.layer.name if self.layer is not None else None}'>"
        )
        dict_data = {
            f"ramdata_{self.identifier}": {
                "barcodes": {
                    "filter": self.bc.filter is not None,
                    "number_of_entries": self.bc.meta._n_rows_unfiltered,
                    "number_of_entries_after_applying_filter": self.bc.meta.n_rows,
                    "metadata": {
                        "columns": sorted(self.bc.columns),
                        "settings": {
                            "path_folder_zdf": self.bc.meta._path_folder_zdf,
                            "path_folder_mask": self.bc.meta._path_folder_mask,
                            "flag_use_mask_for_caching": self.bc.meta.flag_use_mask_for_caching,
                            "flag_retrieve_categorical_data_as_integers": self.bc.meta.flag_retrieve_categorical_data_as_integers,
                            "flag_load_data_after_adding_new_column": self.bc.meta._flag_load_data_after_adding_new_column,
                            "int_num_bytes_in_a_chunk": self.bc.meta.int_num_bytes_in_a_chunk,
                        },
                    },
                },
                "features": {
                    "filter": self.ft.filter is not None,
                    "number_of_entries": self.ft.meta._n_rows_unfiltered,
                    "number_of_entries_after_applying_filter": self.ft.meta.n_rows,
                    "metadata": {
                        "columns": sorted(self.ft.columns),
                        "settings": {
                            "path_folder_zdf": self.ft.meta._path_folder_zdf,
                            "path_folder_mask": self.ft.meta._path_folder_mask,
                            "flag_use_mask_for_caching": self.ft.meta.flag_use_mask_for_caching,
                            "flag_retrieve_categorical_data_as_integers": self.ft.meta.flag_retrieve_categorical_data_as_integers,
                            "flag_load_data_after_adding_new_column": self.ft.meta._flag_load_data_after_adding_new_column,
                            "int_num_bytes_in_a_chunk": self.ft.meta.int_num_bytes_in_a_chunk,
                        },
                    },
                },
                "currently_active_layer": None
                if self.layer is None
                else {
                    "name": self.layer.name,
                    "modes": list(self.layer.modes),
                    "total_number_of_records": self.layer.int_num_records,
                    "settings": {
                        "int_num_cpus_for_fetching_data": self.layer.int_num_cpus,
                    },
                },
                "layers": sorted(self.layers),
                "models": self.models,
                "settings": {
                    "identifier": self.identifier,
                    "has_mask": self.has_mask,
                    "is_component": self.is_component,
                    "is_combined": self.is_combined,
                    "read_only": self._mode == "r",
                    "path_folder_ramdata": self._path_folder_ramdata,
                    "path_folder_ramdata_mask": self._path_folder_ramdata_mask,
                    "verbose": self.verbose,
                    "debugging": self.flag_debugging,
                    "int_num_cpus": self.int_num_cpus,
                    "int_num_cpus_for_fetching_data": self._int_num_cpus_for_fetching_data,
                    "int_num_entries_for_each_weight_calculation_batch": self.int_num_entries_for_each_weight_calculation_batch,
                    "int_total_weight_for_each_batch": self.int_total_weight_for_each_batch,
                    "flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx": self.flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx,
                },
            }
        }
        component_header = "h2" if index_component is None else "h5"
        name_title = f'<{component_header}>RamData{"" if index_component is None else f"-component ({index_component})"}</{component_header}><div><tt>{self.__repr__( )[ 1 : -1 ]}</tt></div>'  # use 0-based coordinates
        str_html = html_from_dict(
            dict_data=dict_data, name_dict=name_title
        )  # retrieve html representation of current RamData
        if self.is_combined:
            # %% COMBINED %%
            for index, ram in enumerate(self._l_ramdata):  # for each component RamData
                str_html += ram._repr_html_(index_component=index)
        return str_html

    def create_view(self):
        """# 2022-07-06 21:17:56
        create view of the RamData using the current filter settings (load dictionaries for coordinate conversion for filtered barcodes/features)
        """
        self.ft.create_view()
        self.bc.create_view()

    def destroy_view(self):
        """# 2022-07-05 22:55:22
        unload dictionaries for coordinate conversion for filtered barcodes/features, destroying the current view
        """
        self.ft.destroy_view()
        self.bc.destroy_view()

    def __enter__(self):
        """# 2022-07-16 15:53:13
        creating a view of RamData using the current filter settings
        """
        self.create_view()  # create view
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """# 2022-07-16 15:54:59
        destroy the current view of RamData
        """
        self.destroy_view()  # destroy view

    def compose_filters(
        self,
        l_entry_bc=[],
        l_entry_ft=[],
        flag_use_str_repr_bc=False,
        flag_use_str_repr_ft=False,
    ):
        """# 2022-07-16 17:10:07
        for the given 'barcodes'/'features' entries, compose filters containing the entries, and apply the filters.

        === inputs ===
        'flag_use_str_repr_bc' = False, 'flag_use_str_repr_ft' = False : flags indicating whether to use string representation of the retrieved entries later

        === outputs ===
        bitarray mask of mapped entries and list of string representations (if available. if string representations were not used to retrieve entries, None will be returned for the list object).
        """
        # retrieve flags indicating that the string representations are not loaded
        flag_str_not_loaded_bc = self.bc.map_int is None
        flag_str_not_loaded_ft = self.ft.map_int is None

        """ retrieve filters and string representations for the queried entries """
        """ barcode """
        # load str representation data
        if flag_use_str_repr_bc and flag_str_not_loaded_bc:
            self.bc.load_str()
        # retrieve filter for the queried entries
        ba_entry_bc = self.bc[l_entry_bc]

        # retrieve str representations of the queried entries
        l_str_bc = None
        if flag_use_str_repr_bc:
            dict_map = self.bc.map_int
            l_str_bc = list(dict_map[i] for i in BA.to_integer_indices(ba_entry_bc))
            del dict_map
        if (
            flag_str_not_loaded_bc
        ):  # if 'str' data was not loaded, unload the str data once all necessary data has been retrieved
            self.bc.unload_str()

        """ feature """
        # load str representation data
        if flag_use_str_repr_ft and flag_str_not_loaded_ft:
            self.ft.load_str()
        # retrieve filter for the queried entries
        ba_entry_ft = self.ft[l_entry_ft]
        # retrieve str representations of the queried entries
        l_str_ft = None
        if flag_use_str_repr_ft:
            dict_map = self.ft.map_int
            l_str_ft = list(dict_map[i] for i in BA.to_integer_indices(ba_entry_ft))
            del dict_map
        if (
            flag_str_not_loaded_ft
        ):  # if 'str' data was not loaded, unload the str data once all necessary data has been retrieved
            self.ft.unload_str()

        return (
            ba_entry_bc,
            l_str_bc,
            ba_entry_ft,
            l_str_ft,
        )  # return composed filters and mapped string representations (if available)

    def __getitem__(self, args):
        """# 2023-02-17 19:54:59
        please include 'str' in 'barcode_column' and 'feature_column' in order to use string representations in the output AnnData object

        possible usages:

        [ name_layer, barcode_index, barcode_column, feature_index, feature_column ]
        [ barcode_index, barcode_column, feature_index, feature_column ]
        'barcode_column' and 'feature_column' can include multi-dimensional data
        for example,
            [ 'str', { 'X_pca' : slice( 0, 10 ), 'X_umap', : None } ] as 'barcode_column' will include X_umap and X_pca in obsm in the resulting anndata object
            [ 'str', { 'X_pca' : slice( 0, 10 ), { 'X_umap' } ] as 'barcode_column' will also include X_umap and X_pca in obsm in the resulting anndata object
        """
        import anndata

        assert isinstance(args, tuple)  # more than one arguments should be given
        # if the first argument appears to be 'name_layer', load the layer and drop the argument
        if (
            args[0] is None
        ):  # if None is given as the first argument, does not load a layer
            args = args[1:]
        elif (
            isinstance(args[0], str) and args[0] in self.layers
        ):  # if a valid name_layer was given as the first argument
            self.layer = args[0]
            args = args[1:]
        assert (
            len(args) <= 4
        )  # assumes layer has been loaded, and only arguments are for barcode/feature indexing

        args = list(args) + list(
            [] for i in range(4 - len(args))
        )  # make the number of arguments to 4
        l_entry_bc, l_col_bc, l_entry_ft, l_col_ft = args  # parse arguments

        # backup the filters
        ba_filter_bc_backup = self.bc.filter
        ba_filter_ft_backup = self.ft.filter

        # retrieve flags for using string representations in the output
        flag_use_str_repr_bc = "str" in l_col_bc
        flag_use_str_repr_ft = "str" in l_col_ft

        # compose filters from the queried entries
        ba_entry_bc, l_str_bc, ba_entry_ft, l_str_ft = self.compose_filters(
            l_entry_bc=l_entry_bc,
            l_entry_ft=l_entry_ft,
            flag_use_str_repr_bc=flag_use_str_repr_bc,
            flag_use_str_repr_ft=flag_use_str_repr_ft,
        )

        # set barcode/feature filters for the queried entries
        self.bc.filter = ba_entry_bc
        self.ft.filter = ba_entry_ft

        # retrieve meta data as dataframes
        df_obs = self.bc.meta.get_df(*l_col_bc)
        if flag_use_str_repr_bc:  # add string representations
            df_obs.index = l_str_bc
            del l_str_bc
        df_var = self.ft.meta.get_df(*l_col_ft)
        if flag_use_str_repr_ft:  # add string representations
            df_var.index = l_str_ft
            del l_str_ft

        # build output AnnData object
        adata = anndata.AnnData(
            obs=df_obs, var=df_var
        )  # in anndata.X, row = barcode, column = feature # set obs and var with integer index values

        # add obsm/varm
        for ax, name_attr, l in zip(
            [self.ft, self.bc], ["varm", "obsm"], [l_col_ft, l_col_bc]
        ):
            for e in l:
                if isinstance(e, set):  # retrieve all data in the secondary axis
                    for name_col in e:
                        if name_col in ax.meta:  # if the column exists in the metadata
                            getattr(adata, name_attr)[name_col] = ax.meta[name_col]
                elif isinstance(e, dict):  # indexing through secondary axis
                    for name_col in e:
                        if name_col in ax.meta:  # if the column exists in the metadata
                            getattr(adata, name_attr)[name_col] = (
                                ax.meta[name_col]
                                if e[name_col] is None
                                else ax.meta[name_col, None, e[name_col]]
                            )  # if e[ name_col ] is None, load all data on the secondary axis

        """
        retrieve and add count data from RamDataLayer
        """
        if self.layer is not None:
            # retrieve ramtx for retrieving data
            rtx = self.layer.select_ramtx(ba_entry_bc, ba_entry_ft)

            # initialize and destroy the view after retrieving the count matrix
            with self as view:  # load 'dict_change' for coordinate conversion according to the given filters, creating the view of the RamData
                # retrieve count data
                X = rtx.get_sparse_matrix(
                    []
                )  # retrieve count data for all entries currently active in the filter

            adata.X = X  # add count data
            del X

        # restore the filters once the data retrieval has been completed
        self.bc.filter = ba_filter_bc_backup
        self.ft.filter = ba_filter_ft_backup

        return adata  # return resulting AnnData

    def save(self, *l_name_adata):
        """wrapper of AnnDataContainer.save"""
        self.ad.update(*l_name_adata)

    """ <CORE METHODS> """

    def summarize(
        self,
        name_layer: str,
        axis: Union[int, str],
        summarizing_func: Callable,
        l_name_col_summarized: Union[list, None] = None,
        str_prefix: Union[str, None] = None,
        str_suffix: str = "",
    ):
        """# 2023-03-26 12:29:02
        this function summarize entries of the given axis (0 = barcode, 1 = feature) using the given function

        example usage: calculate total sum, standard deviation, pathway enrichment score calculation, etc.

        =========
        inputs
        =========
        'name_layer' : name of the data in the given RamData object to summarize
        axis : Union[ int, str ]
               # 0, 'b', 'bc', 'barcode' or 'barcodes' for applying a given summarizing function for barcodes
               # 1, 'f', 'ft', 'feature' or 'features' for applying a given summarizing function for features
        'summarizing_func' : function object. a function that takes a RAMtx output and return a dictionary containing 'name_of_summarized_data' as key and 'value_of_summarized_data' as value. the resulting summarized outputs will be added as metadata of the given Axis (self.bc.meta or self.ft.meta)

                    summarizing_func( self, int_entry_of_axis_for_querying, arr_int_entries_of_axis_not_for_querying, arr_value ) -> dictionary containing 'key' as summarized metric name and 'value' as a summarized value for the entry. if None is returned, the summary result for the entry will be skipped.

                    a list of pre-defined functions are the followings :
                    'sum' :
                            calculate the total sum (and mean) for each entry
                            useful for initial barcode filtering

                            returns: 'sum', 'mean'

                    'sum_and_dev' :
                            calculate the total sum (and mean) and the total deviation (and variance) for each entry
                            deviation = sum( ( X - X_mean ) ** 2 )
                            variance = sum( ( X - X_mean ) ** 2 ) / ( total_num_entry - 1 )
                            useful for identifying informative features

                            returns: 'sum', 'mean', 'deviation', 'variance'

                    'count_min_max' :
                            calculate the min and max values, and count the number of active barcodes/features (that were not indexed) for the entry of the indexed axis

                            returns: 'count', 'max', 'min'

        'l_name_col_summarized' : list of column names returned by 'summarizing_func'. by default (when None is given), the list of column names will be inferred by observing output when giving zero values as inputs
        'str_prefix' : an additional prefix on the new columns of the axis metadata. if None is given (by default), f"{name_layer}_" will be used as a prefix
        'str_suffix' : an additional suffix of the new columns of the axis metadata that will contain summarized results
            * the output column name will be f"{str_prefix}{e}{str_suffix}", where {e} is the key of the dictionary returned by the 'summarizing_func'

        ** warning ** existing columns will be overwritten!

        =========
        outputs
        =========
        the summarized metrics will be added to appropriate dataframe attribute of the AnnData of the current RamData (self.adata.obs for axis = 0 and self.adata.var for axis = 1).
        the column names will be constructed as the following :
            f"{name_layer}_{key}"
        if the column name already exist in the dataframe, the values of the columns will be overwritten
        """
        """
        1) Prepare
        """
        # check the validility of the input arguments
        if name_layer not in self.layers:
            if self.verbose:
                logger.error(
                    f"invalid argument 'name_layer' : '{name_layer}' does not exist."
                )
            return -1
        if axis not in {
            0,
            "barcode",
            1,
            "feature",
            "barcodes",
            "features",
            "bc",
            "ft",
            "b",
            "f",
        }:
            if self.verbose:
                logger.error(f"invalid argument 'axis' : '{axis}' is invalid.")
            return -1
        # set layer
        self.layer = name_layer
        # handle inputs
        flag_summarizing_barcode = self._determine_axis(
            axis
        )  # retrieve a flag indicating whether the data is summarized for each barcode or not
        # set default 'str_prefix' for new column names
        if not isinstance(str_prefix, str):
            str_prefix = f"{name_layer}_"

        # retrieve the total number of entries in the axis that was not indexed (if calculating average expression of feature across barcodes, divide expression with # of barcodes, and vice versa.)
        int_total_num_entries_not_indexed = (
            self.ft.meta.n_rows if flag_summarizing_barcode else self.bc.meta.n_rows
        )

        int_num_threads = self.int_num_cpus  # set the number of threads
        if summarizing_func == "sum":

            def summarizing_func(
                self,
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            ):
                """# 2022-08-01 21:05:06
                calculate sum of the values of the current entry

                assumes 'int_num_records' > 0
                """
                int_num_records = len(
                    arr_value
                )  # retrieve the number of records of the current entry
                dict_summary = {
                    "sum": np.sum(arr_value)
                    if int_num_records > 30
                    else sum(arr_value),
                    "num_nonzero_values": int_num_records,
                }  # if an input array has more than 30 elements, use np.sum to calculate the sum
                dict_summary["mean"] = (
                    dict_summary["sum"] / int_total_num_entries_not_indexed
                )  # calculate the mean
                return dict_summary

        elif summarizing_func == "sum_and_dev":

            def summarizing_func(
                self,
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            ):
                """# 2022-08-01 21:05:02
                calculate sum and deviation of the values of the current entry

                assumes 'int_num_records' > 0
                """
                int_num_records = len(
                    arr_value
                )  # retrieve the number of records of the current entry
                dict_summary = {
                    "sum": np.sum(arr_value)
                    if int_num_records > 30
                    else sum(arr_value),
                    "num_nonzero_values": int_num_records,
                }  # if an input array has more than 30 elements, use np.sum to calculate the sum
                dict_summary["mean"] = (
                    dict_summary["sum"] / int_total_num_entries_not_indexed
                )  # calculate the mean
                arr_dev = (
                    arr_value - dict_summary["mean"]
                ) ** 2  # calculate the deviation
                dict_summary["deviation"] = (
                    np.sum(arr_dev) if int_num_records > 30 else sum(arr_dev)
                )
                dict_summary["variance"] = (
                    dict_summary["deviation"] / (int_total_num_entries_not_indexed - 1)
                    if int_total_num_entries_not_indexed > 1
                    else np.nan
                )
                return dict_summary

        elif summarizing_func == "count_min_max":
            int_min_num_records_for_numpy = 30

            def summarizing_func(
                self,
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            ):
                """# 2022-07-27 15:29:07
                calculate sum and deviation of the values of the current entry

                assumes 'int_num_records' > 0
                """
                int_num_records = len(
                    arr_value
                )  # retrieve the number of records of the current entry
                dict_summary = {
                    "count": int_num_records,
                    "max": np.max(arr_value)
                    if int_num_records > int_min_num_records_for_numpy
                    else max(arr_value),
                    "min": np.min(arr_value)
                    if int_num_records > int_min_num_records_for_numpy
                    else min(arr_value),
                }  # if an input array has more than 'int_min_num_records_for_numpy' elements, use numpy to calculate min/max values
                return dict_summary

        elif not hasattr(
            summarizing_func, "__call__"
        ):  # if 'summarizing_func' is not a function, report error message and exit
            if self.verbose:
                logger.info(f"given summarizing_func is not a function, exiting")
            return -1
        # infer 'l_name_col_summarized'
        if l_name_col_summarized is None:
            # retrieve the list of key values returned by 'summarizing_func' by applying dummy values
            arr_dummy_one, arr_dummy_zero = np.ones(10, dtype=int), np.zeros(
                10, dtype=int
            )
            l_name_col_summarized = list(
                summarizing_func(self, 0, arr_dummy_zero, arr_dummy_one)
            )
        l_name_col_summarized = sorted(
            l_name_col_summarized
        )  # retrieve the list of key values of an dict_res result returned by 'summarizing_func'
        l_name_col_summarized_with_name_layer_prefix_and_suffix = list(
            f"{str_prefix}{e}{str_suffix}" for e in l_name_col_summarized
        )  # retrieve the name_col containing summarized data with f'{name_layer}_' prefix

        # retrieve Axis object to summarize
        ax = self.bc if flag_summarizing_barcode else self.ft

        if self.use_locking:  # %% FILE LOCKING %%
            release_locks_for_metadata_columns = (
                self.acquire_locks_for_metadata_columns(
                    axis=axis,
                    l_name_col=l_name_col_summarized_with_name_layer_prefix_and_suffix,
                )
            )
        try:
            # retrieve RAMtx object to summarize
            rtx = self.layer.get_ramtx(not flag_summarizing_barcode)
            if rtx is None:
                if self.verbose:
                    logger.error(
                        f"it appears that the current layer {self.layer.name} appears to be empty, exiting"
                    )
                return

            # define functions for multiprocessing step
            def process_batch(pipe_receiver_batch, pipe_sender_result):
                """# 2022-05-08 13:19:07
                summarize a given list of entries, and send summarized result through a pipe
                """
                # retrieve fork-safe RAMtx
                rtx_fork_safe = (
                    rtx.get_fork_safe_version()
                )  # load zarr_server (if RAMtx contains remote data source) to be thread-safe

                while True:
                    batch = pipe_receiver_batch.recv()
                    if batch is None:
                        break
                    int_num_processed_records, l_int_entry_current_batch = (
                        batch["int_accumulated_weight_current_batch"],
                        batch["l_int_entry_current_batch"],
                    )  # parse batch

                    # retrieve the number of index_entries
                    int_num_entries_in_a_batch = len(l_int_entry_current_batch)

                    if int_num_entries_in_a_batch == 0:
                        logger.info("empty batch detected")

                    # iterate through the data of each entry
                    dict_data = dict(
                        (name_col, []) for name_col in l_name_col_summarized
                    )  # collect results
                    l_int_entry_of_axis_for_querying = (
                        []
                    )  # collect list of queried entries with valid results
                    for (
                        int_entry_of_axis_for_querying,
                        arr_int_entry_of_axis_not_for_querying,
                        arr_value,
                    ) in zip(
                        *rtx_fork_safe[l_int_entry_current_batch]
                    ):  # retrieve data for the current batch
                        # retrieve summary for the entry
                        dict_res = summarizing_func(
                            self,
                            int_entry_of_axis_for_querying,
                            arr_int_entry_of_axis_not_for_querying,
                            arr_value,
                        )  # summarize the data for the entry
                        # if the result empty, does not collect the result
                        if dict_res is None:
                            continue
                        # collect the result
                        # collect the int_entry with a valid result
                        l_int_entry_of_axis_for_querying.append(
                            int_entry_of_axis_for_querying
                        )
                        # collect the result
                        for name_col in l_name_col_summarized:
                            dict_data[name_col].append(
                                dict_res[name_col] if name_col in dict_res else np.nan
                            )
                    pipe_sender_result.send(
                        (
                            int_num_processed_records,
                            l_int_entry_of_axis_for_querying,
                            dict_data,
                        )
                    )  # send information about the output file

                # destroy zarr servers
                rtx_fork_safe.terminate_spawned_processes()

            # initialize the progress bar
            pbar = progress_bar(
                desc=f"{name_layer} / {'barcodes' if flag_summarizing_barcode else 'features'}",
                total=rtx.get_total_num_records(
                    int_num_entries_for_each_weight_calculation_batch=self.int_num_entries_for_each_weight_calculation_batch,
                    flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=self.flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx,
                ),
            )
            zdf_meta_without_locking = ax.meta.get_fork_safe_version(
                flag_use_locking=False
            )  # retrieve ZarrDataFrame metadata that does not using locking

            def post_process_batch(res):
                """# 2022-07-06 03:21:49"""
                (
                    int_num_processed_records,
                    l_int_entry_of_axis_for_querying,
                    dict_data,
                ) = res  # parse result
                # exit if no result has been collected
                if len(l_int_entry_of_axis_for_querying) == 0:
                    return

                pbar.update(int_num_processed_records)  # update the progress bar

                # update metadata
                df = pd.DataFrame(
                    dict_data, index=l_int_entry_of_axis_for_querying
                )  # compose dataframe using 'dict_data'
                df.rename(
                    columns=dict(
                        (name_col, name_col_with_prefix_and_suffix)
                        for name_col, name_col_with_prefix_and_suffix in zip(
                            l_name_col_summarized,
                            l_name_col_summarized_with_name_layer_prefix_and_suffix,
                        )
                    ),
                    inplace=True,
                )  # rename column names
                zdf_meta_without_locking.update(
                    df, flag_use_index_as_integer_indices=True
                )
                del df

            # summarize the RAMtx using multiple processes
            rtx_fork_safe = (
                rtx.get_fork_safe_version()
            )  # get fork-safe version of rtx (batch generator uses a separate process to retrieve a batch, which requires rtx object to be used in a forked process)
            try:
                bk.Multiprocessing_Batch_Generator_and_Workers(
                    rtx_fork_safe.batch_generator(
                        ax.filter,
                        int_num_entries_for_each_weight_calculation_batch=self.int_num_entries_for_each_weight_calculation_batch,
                        int_total_weight_for_each_batch=self.int_total_weight_for_each_batch,
                        flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=self.flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx,
                    ),
                    process_batch,
                    post_process_batch=post_process_batch,
                    int_num_threads=int_num_threads,
                    int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
                )
            finally:
                # terminate the spawned processes
                rtx_fork_safe.terminate_spawned_processes()
                zdf_meta_without_locking.terminate_spawned_processes()
                pbar.close()  # close the progress bar
        finally:
            if self.use_locking:  # %% FILE LOCKING %%
                release_locks_for_metadata_columns()

        # update attributes of metadata ZarrDataFrame # locking & metadata was updated by a cloned object of the ZarrDataFrame, and the attributes should be updated
        ax.meta.get_metadata()
        # report results
        if self.verbose:
            logger.info(
                f"summarize operation of {name_layer} in the '{'barcode' if flag_summarizing_barcode else 'feature'}' axis was completed"
            )

    def apply(
        self,
        name_layer,
        name_layer_new,
        func=None,
        mode_instructions="sparse_for_querying_features",
        path_folder_ramdata_output=None,
        dtype_of_row_and_col_indices=np.int32,
        dtype_of_value=np.float64,
        int_num_threads=None,
        flag_survey_weights=True,
        flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=True,
        int_num_of_records_in_a_chunk_zarr_matrix=500000,
        int_num_of_entries_in_a_chunk_zarr_matrix_index=1000,
        chunks_dense=(2000, 1000),
        dtype_dense_mtx=np.float64,
        dtype_sparse_mtx=np.float64,
        dtype_sparse_mtx_index=np.float64,
        dict_metadata_description: Union[dict, None] = dict(),
    ):
        """# 2023-02-21 01:38:46
        this function apply a function and/or filters to the records of the given data, and create a new data object with 'name_layer_new' as its name.

        example usage: calculate normalized count data, perform log1p transformation, cell filtering, etc.

        =========
        inputs
        =========

        'name_layer' : (required) name of the data in the given RamData object to analyze
        'name_layer_new' : (required) name of the new data for the paired RAMtx objects that will contains transformed values (the outputs of the functions applied to previous data values). The disk size of the RAMtx objects can be larger or smaller than the RAMtx objects of 'name_layer'. please make sure that sufficient disk space remains before calling this function.
        'path_folder_ramdata_output' : (Default: store inside the current RamData). The directory of the RamData object that will contain the outputs (paired RAMtx objects). if integer representations of features and barcodes are updated from filtering, the output RAMtx is now incompatible with the current RamData and should be stored as a separate RamData object. The output directory of the new RamData object can be given through this argument.
        'func' : function object or string (Default: identity) a function that takes a tuple of two integers (integer representations of barcode and feature) and another integer or float (value) and returns a modified record. Also, the current RamData object will be given as the first argument (self), and attributes of the current RamData can be used inside the function

                 func( self, int_entry_of_axis_for_querying, arr_int_entries_of_axis_not_for_querying, arr_value ) -> int_entry_of_axis_for_querying, arr_int_entries_of_axis_not_for_querying, arr_value

                 if None is returned, the entry will be discarded in the output RAMtx object. Therefore, the function can be used to both filter or/and transform values

                 a list of pre-defined functions are the followings:
                 'log1p' :
                          X_new = log_10(X_old + 1)
                 'ident' or None :
                          X_new = X_old

                separate functions for processing feature-by-feature data and barcode-by-barcode data can be given using either dictionary or tuple.
                    func = ( func_bc, func_ft )
                                or
                    func = { 'barcodes' : func_bc, 'features' : func_ft }

        'mode_instructions' : instructions for converting modes of the ramtx objects.
                it is a nested list with the following structure
                [ [ 'ramtx_mode_source', 'ramtx_mode_sink' (or a list of 'ramtx_mode_sink') ], ... ]
                    where 'ramtx_mode_source' is the mode of the ramtx of the 'name_layer' layer from which data will be fetched, and 'ramtx_mode_sink' is the mode of the new ramtx of the 'name_layer_new' layer to which the fetched data will be transformed according to the function and written.


                examples:

                mode_instructions = 'sparse_for_querying_features'
                    ... is equivalent to ...
                mode_instructions = [ [ 'sparse_for_querying_features' ] ]
                --> 'sparse_for_querying_features' ramtx object of the 'name_layer' layer converted to 'sparse_for_querying_features' ramtx object of the 'name_layer_new' layer (same ramtx mode)

                mode_instructions = [ 'sparse_for_querying_features', [ 'sparse_for_querying_features', 'dense' ] ]
                    ... is equivalent to ...
                mode_instructions = [ [ 'sparse_for_querying_features', [ 'sparse_for_querying_features', 'dense' ] ] ]
                --> 'sparse_for_querying_features' ramtx object of the 'name_layer' layer converted to 'sparse_for_querying_features' and 'dense' ramtx object of the 'name_layer_new' layer

                mode_instructions = [ [ 'sparse_for_querying_features', 'sparse_for_querying_features' ],
                                      [ 'sparse_for_querying_features', 'dense' ] ]
                --> 'sparse_for_querying_features' ramtx object of the 'name_layer' layer converted to 'sparse_for_querying_features' and 'dense' ramtx object of the 'name_layer_new' layer. however, for this instruction, 'sparse_for_querying_features' will be read twice, which will be redundant and less efficient.

                mode_instructions = [ [ 'sparse_for_querying_features' ],
                                      [ 'dense', [ 'sparse_for_querying_features', 'dense', 'sparse_for_querying_barcodes' ] ] ]
                --> 'sparse_for_querying_features' > 'sparse_for_querying_features'
                    'dense_for_querying_features' > 'sparse_for_querying_features', 'dense' (1 read, 2 write) # by default, dense is set for querying features, but it can be changed so that dense matrix can be constructed by querying barcodes from the source dense ramtx object.
                    'dense_for_querying_barcodes' > 'sparse_for_querying_barcodes' of 'name_layer_new'

                mode_instructions = [ [ 'dense_for_querying_features', 'dense_for_querying_barcode' ],
                                      [ 'dense', [ 'sparse_for_querying_features', 'dense', 'sparse_for_querying_barcodes' ] ] ]
                --> 'dense_for_querying_features' > 'dense'
                    'dense_for_querying_features' > 'sparse_for_querying_features' # since 'dense' > 'dense' conversion already took place, (1 read, 1 write) operation will be performed
                    'dense_for_querying_barcodes' > 'sparse_for_querying_barcodes'

                in summary, (1) up to three operations will be performed, to construct three ramtx modes of the resulting layer, (2) the instructions at the front has higher priority, and (3) querying axis of dense can be specified or skipped (in those cases, default will be used)

                Of note, output to 'Dense' format can be slow for remote file systems (e.g. Amazon S3), since writing the dense Zarr array will rely on a file-locking using a directory on the remote file system by default. Therefore, providing the path to store file-system based lock is highly recommended for creating a 'dense' matrix output.

                Additionally, the follwoing arguments can be given with for each instruction.
                    'dtype_of_row_and_col_indices',  'dtype_of_value',  'int_num_of_records_in_a_chunk_zarr_matrix',  'int_num_of_entries_in_a_chunk_zarr_matrix_index',  'chunks_dense',  'dtype_dense_mtx',  'dtype_sparse_mtx',  'dtype_sparse_mtx_index',
                For example,
                mode_instructions = [ [ 'dense_for_querying_features', 'dense_for_querying_barcode', { 'int_num_of_entries_in_a_chunk_zarr_matrix_index' : 1000 } ],
                                      [ 'dense', [ 'sparse_for_querying_features', 'dense', 'sparse_for_querying_barcodes' ], { 'chunks_dense' : ( 1000, 1000 ) } ] ]
                can be used to change parameters for each instruction.



        'int_num_threads' : the number of CPUs to use. by default, the number of CPUs set by the RamData attribute 'int_num_cpus' will be used.
        'flag_survey_weights' : survey the weights of the output RAMtx objects
        'dtype_of_row_and_col_indices', 'dtype_of_value' : the dtype of the output matrix
        int_num_of_records_in_a_chunk_zarr_matrix = 500000, int_num_of_entries_in_a_chunk_zarr_matrix_index = 1000, chunks_dense = ( 2000, 1000 ) : determines the chunk size of the output ramtx objects
        dtype_dense_mtx = np.float64, dtype_sparse_mtx = np.float64, dtype_sparse_mtx_index = np.float64 : determines the output dtype
        dict_metadata_description : Union[ dict, None ] = dict( ) # the metadata (optional) of the newly created output layer.

        =================
        input attributes
        =================
        the attributes shown below or any other custom attributes can be used internally as READ-ONLY data objects when executing the given 'func'.

        For example, one can define the following function:

        ram = RamData( path_folder_to_ramdata ) verbose : bool = True,
        ram.a_variable = 10
        def func( self, int_entry_of_axis_for_querying, arr_int_entries_of_axis_not_for_querying, arr_value ) :
            return self, int_entry_of_axis_for_querying, arr_int_entries_of_axis_not_for_querying, arr_value * self.a_variable

        # IMPORTANT. since these attributes will be used across multiple processes, only the single RamData 'Apply' operation can be run on Ram data. (or all RamData.Apply operations should use the same attributes containing the same values)
        """
        # handle inputs
        if int_num_threads is None:
            int_num_threads = self.int_num_cpus
        if name_layer_new is None:
            name_layer_new = name_layer
        flag_new_layer_added_to_the_current_ramdata = False
        if path_folder_ramdata_output is None:
            flag_new_layer_added_to_the_current_ramdata = True  # set flag indicating that the new layer will be added to the current ramdata object (or the mask of the current ramdata object)
            path_folder_ramdata_output = (
                self._path_folder_ramdata_modifiable
            )  # retrieve path to the modifiable ramdata object
            if path_folder_ramdata_output is None:
                if self.verbose:
                    logger.error("current RamData object is not modifiable, exiting")
                return
        # retrieve flags
        flag_update_a_layer = (
            name_layer_new == name_layer
            and path_folder_ramdata_output == self._path_folder_ramdata_modifiable
        )  # a flag indicating whether a layer of the current ramdata is updated (input ramdata == output ramdata and input layer name == output layer name).
        # retrieve paths
        path_folder_layer_new = f"{path_folder_ramdata_output}{name_layer_new}/"  # compose the output directory of the output ramdata layer

        # open (and initialize) the new (output) layer
        layer_new = RamDataLayer(
            path_folder_ramdata_output,
            name_layer_new,
            ramdata=None,
            dtype_of_feature_and_barcode_indices=self._dtype_of_feature_and_barcode_indices,
            dtype_of_values=self._dtype_of_values,
            int_num_cpus=self._int_num_cpus_for_fetching_data,
            verbose=self.verbose,
            mode=self._mode,
            path_folder_ramdata_mask=self._path_folder_ramdata_mask,
            flag_is_read_only=self._flag_is_read_only,
        )

        # parse 'func' or set default functions, retrieving 'func_bc' and 'func_ft'.
        if hasattr(
            func, "__call__"
        ):  # if a single function has been given, use the function for 'func_bc' and 'func_ft'
            func_bc = func
            func_ft = func
        elif isinstance(
            func, dict
        ):  # if 'func' is dictionary, parse functions for each axes
            func_bc = func["barcodes"]
            func_ft = func["features"]
        elif isinstance(func, tuple):
            assert (
                len(func) == 2
            )  # if 'func' is tuple, the length of 'func' should be 2
            func_bc, func_ft = func
        elif func == "ident" or func is None:
            # define identity function if 'func' has not been given
            def func_bc(
                self,
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            ):
                return (
                    int_entry_of_axis_for_querying,
                    arr_int_entries_of_axis_not_for_querying,
                    arr_value,
                )

            func_ft = func_bc  # use the same function for the other axis
        elif func == "log1p":

            def func_bc(
                self,
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            ):
                return (
                    int_entry_of_axis_for_querying,
                    arr_int_entries_of_axis_not_for_querying,
                    np.log10(arr_value + 1),
                )

            func_ft = func_bc  # use the same function for the other axis

        # check the validility of the input arguments
        if not name_layer in self.layers:
            if self.verbose:
                logger.error(
                    f"[RamData.Apply] invalid argument 'name_layer' : '{name_layer}' does not exist."
                )
            return -1

        """ set 'name_layer' as a current layer of RamData """
        self.layer = name_layer

        if self.use_locking:  # %% FILE LOCKING %%
            # locks of the input and output layers
            path_lock_layer_input = f"{self.layer.path_folder_ramdata_layer}.lock"
            path_lock_layer_output = f"{path_folder_layer_new}.lock"
            self._zsls.acquire_lock(
                path_lock_layer_input
            )  # acquire locks for the input layer
            self._zsls.acquire_lock(
                path_lock_layer_output
            )  # acquire locks for the output layer

        def RAMtx_Apply(
            self,
            rtx,
            func,
            flag_dense_ramtx_output,
            flag_sparse_ramtx_output,
            int_num_threads,
            dict_setting,
        ):
            """# 2023-02-21 01:38:34
            inputs
            =========

            'rtx': an input RAMtx object
            'dict_setting' : a dictionary containing settings for the RAMtx_Apply operation
            """
            """ prepare """
            # parse the given setting
            dtype_of_row_and_col_indices = dict_setting["dtype_of_row_and_col_indices"]
            dtype_of_value = dict_setting["dtype_of_value"]
            int_num_of_records_in_a_chunk_zarr_matrix = dict_setting[
                "int_num_of_records_in_a_chunk_zarr_matrix"
            ]
            int_num_of_entries_in_a_chunk_zarr_matrix_index = dict_setting[
                "int_num_of_entries_in_a_chunk_zarr_matrix_index"
            ]
            chunks_dense = dict_setting["chunks_dense"]
            dtype_dense_mtx = dict_setting["dtype_dense_mtx"]
            dtype_sparse_mtx = dict_setting["dtype_sparse_mtx"]
            dtype_sparse_mtx_index = dict_setting["dtype_sparse_mtx_index"]

            # initialize
            flag_spawn = (
                rtx.contains_remote
            )  # retrieve a flag whether to use a spawned process for operations that are not potentially not fork-safe (but less performant)
            rtx_fork_safe = (
                rtx.get_fork_safe_version()
            )  # retrieve a fork-safe version of a RAMtx
            fs = FileSystemServer(
                flag_spawn=flag_spawn
            )  # initialize a filesystem server
            zms = ZarrMetadataServer(
                flag_spawn=flag_spawn
            )  # initialize zarr metadata server

            ax = (
                self.ft if rtx.is_for_querying_features else self.bc
            )  # retrieve appropriate axis
            ns = (
                dict()
            )  # create a namespace that can safely shared between different scopes of the functions
            ns[
                "int_num_records_written_to_ramtx"
            ] = 0  # initlaize the total number of records written to ramtx object
            # create a temporary folder
            path_folder_temp = f"{self.path_folder_temp}tmp{bk.UUID( )}/"  # retrieve temporary folder specific to the current run
            fs.filesystem_operations("mkdir", path_folder_temp, exist_ok=True)
            # retrieve the number of entries for each axis for the output RAMtx object
            int_num_features = (
                len(self.ft.m) if self.ft.is_view_active else rtx._int_num_features
            )
            int_num_barcodes = (
                len(self.bc.m) if self.bc.is_view_active else rtx._int_num_barcodes
            )
            """ initialize output ramtx objects """
            """ %% DENSE %% """
            if flag_dense_ramtx_output:  # if dense output is present
                path_folder_ramtx_dense = f"{path_folder_layer_new}dense/"
                fs.filesystem_operations(
                    "mkdir", path_folder_ramtx_dense, exist_ok=True
                )  # create the output ramtx object folder
                path_folder_ramtx_dense_mtx = f"{path_folder_ramtx_dense}matrix.zarr/"  # retrieve the folder path of the output RAMtx Zarr matrix object.
                # assert not fs.filesystem_operations( 'exists', path_folder_ramtx_dense_mtx ) # output zarr object should NOT exists!
                path_file_lock_mtx_dense = f"{path_folder_temp}lock_{bk.UUID( )}.sync"  # define path to locks for parallel processing with multiple processes
                za_mtx_dense = ZarrServer(
                    path_folder_ramtx_dense_mtx,
                    mode="w",
                    shape=(int_num_barcodes, int_num_features),
                    chunks=chunks_dense,
                    dtype=dtype_dense_mtx,
                    path_process_synchronizer=path_file_lock_mtx_dense,
                    flag_spawn=flag_spawn,
                )  # use the same chunk size of the current RAMtx # initialize the output zarr object
            """ %% SPARSE %% """
            if flag_sparse_ramtx_output:  # if sparse output is present
                mode_sparse = f"sparse_for_querying_{'features' if rtx.is_for_querying_features else 'barcodes'}"
                path_folder_ramtx_sparse = f"{path_folder_layer_new}{mode_sparse}/"
                fs.filesystem_operations(
                    "mkdir", path_folder_ramtx_sparse, exist_ok=True
                )  # create the output ramtx object folder
                path_folder_ramtx_sparse_mtx = f"{path_folder_ramtx_sparse}matrix.zarr/"  # retrieve the folder path of the output RAMtx Zarr matrix object.
                # assert not fs.filesystem_operations( 'exists', path_folder_ramtx_sparse_mtx ) # output zarr object should NOT exists!
                # assert not fs.filesystem_operations( 'exists', f'{path_folder_ramtx_sparse}matrix.index.zarr' ) # output zarr object should NOT exists!
                # open fork-safe zarr objects (initialize zarr objects)
                za_mtx_sparse = ZarrServer(
                    path_folder_ramtx_sparse_mtx,
                    mode="w",
                    shape=(rtx._int_num_records, 2),
                    chunks=(int_num_of_records_in_a_chunk_zarr_matrix, 2),
                    dtype=dtype_sparse_mtx,
                    flag_spawn=flag_spawn,
                )  # use the same chunk size of the current RAMtx
                za_mtx_sparse_index = ZarrServer(
                    f"{path_folder_ramtx_sparse}matrix.index.zarr",
                    mode="w",
                    shape=(rtx.len_axis_for_querying, 2),
                    chunks=(int_num_of_entries_in_a_chunk_zarr_matrix_index, 2),
                    dtype=dtype_sparse_mtx_index,
                    flag_spawn=flag_spawn,
                )  # use the same dtype and chunk size of the current RAMtx

                int_num_records_in_a_chunk_of_mtx_sparse = za_mtx_sparse.chunks[
                    0
                ]  # retrieve the number of records in a chunk of output zarr matrix

                ns[
                    "index_batch_waiting_to_be_written_sparse"
                ] = 0  # index of the batch currently waiting to be written.
                ns["l_res_sparse"] = []

            """ convert matrix values and save it to the output RAMtx object """

            # define functions for multiprocessing step
            def process_batch(pipe_receiver_batch, pipe_sender_result):
                """# 2022-05-08 13:19:07
                retrieve data for a given list of entries, transform values, and save to a Zarr object and index the object, and returns the number of written records and the paths of the written objects (index and Zarr matrix)
                """
                str_uuid = bk.UUID()
                # retrieve fork-safe RAMtx
                rtx_fork_safe = (
                    rtx.get_fork_safe_version()
                )  # retrieve a fork-safe version of a RAMtx

                """ %% DENSE %% """
                if flag_dense_ramtx_output:  # if dense output is present
                    za_mtx_dense = ZarrServer(
                        path_folder_ramtx_dense_mtx, mode="a", flag_spawn=flag_spawn
                    )  # use the same chunk size of the current RAMtx # open a synchronized, fork-safe zarr object

                while True:
                    batch = pipe_receiver_batch.recv()
                    if batch is None:
                        break
                    # initialize
                    path_folder_zarr_output_sparse = None
                    path_file_index_output_sparse = None

                    # parse batch
                    (
                        int_num_processed_records,
                        index_batch,
                        l_int_entry_current_batch,
                    ) = (
                        batch["int_accumulated_weight_current_batch"],
                        batch["index_batch"],
                        batch["l_int_entry_current_batch"],
                    )

                    # retrieve the number of index_entries
                    int_num_entries = len(l_int_entry_current_batch)
                    int_num_records_written = 0  # initialize the record count
                    (
                        l_int_entry_of_axis_for_querying,
                        l_arr_int_entry_of_axis_not_for_querying,
                        l_arr_value,
                    ) = (
                        [],
                        [],
                        [],
                    )  # initializes lists for collecting transformed data

                    """ %% SPARSE %% """
                    if flag_sparse_ramtx_output:  # if sparse output is present
                        # open an Zarr object
                        path_folder_zarr_output_sparse = f"{path_folder_temp}{bk.UUID( )}.zarr/"  # define output Zarr object path
                        za_output_sparse = zarr.open(
                            path_folder_zarr_output_sparse,
                            mode="w",
                            shape=(rtx_fork_safe._int_num_records, 2),
                            chunks=za_mtx_sparse.chunks,
                            dtype=dtype_of_value,
                        )  # 'za_output_sparse' will be stored locally, and ZarrServer will not be used
                        # define an index file
                        path_file_index_output_sparse = f"{path_folder_temp}{bk.UUID( )}.index.tsv.gz"  # define output index file path
                        l_index = []  # collect index

                    # iterate through the data of each entry and transform the data
                    for (
                        int_entry_of_axis_for_querying,
                        arr_int_entry_of_axis_not_for_querying,
                        arr_value,
                    ) in zip(
                        *rtx_fork_safe[l_int_entry_current_batch]
                    ):  # retrieve data for the current batch
                        # transform the values of an entry
                        (
                            int_entry_of_axis_for_querying,
                            arr_int_entry_of_axis_not_for_querying,
                            arr_value,
                        ) = func(
                            self,
                            int_entry_of_axis_for_querying,
                            arr_int_entry_of_axis_not_for_querying,
                            arr_value,
                        )
                        int_num_records = len(
                            arr_value
                        )  # retrieve number of returned records

                        """ %% SPARSE %% """
                        if flag_sparse_ramtx_output:  # if sparse output is present
                            # collect index
                            l_index.append(
                                [
                                    int_entry_of_axis_for_querying,
                                    int_num_records_written,
                                    int_num_records_written + int_num_records,
                                ]
                            )

                        # collect transformed data
                        l_int_entry_of_axis_for_querying.append(
                            int_entry_of_axis_for_querying
                        )
                        l_arr_int_entry_of_axis_not_for_querying.append(
                            arr_int_entry_of_axis_not_for_querying
                        )
                        l_arr_value.append(arr_value)
                        int_num_records_written += (
                            int_num_records  # update the number of records written
                        )

                    """ when returned result is empty, return an empty result """
                    if len(l_arr_int_entry_of_axis_not_for_querying) == 0:
                        pipe_sender_result.send(
                            (
                                index_batch,
                                int_num_processed_records,
                                int_num_records_written,
                                None,
                                None,
                            )
                        )
                        continue
                    else:
                        del (
                            int_entry_of_axis_for_querying,
                            arr_int_entry_of_axis_not_for_querying,
                            arr_value,
                        )  # delete references

                    """ combine results """
                    # combine the arrays
                    arr_int_entry_of_axis_not_for_querying = np.concatenate(
                        l_arr_int_entry_of_axis_not_for_querying
                    )

                    arr_value = np.concatenate(l_arr_value)
                    del l_arr_value  # delete intermediate objects

                    # compose 'arr_int_entry_of_axis_for_querying'
                    arr_int_entry_of_axis_for_querying = np.zeros(
                        len(arr_int_entry_of_axis_not_for_querying),
                        dtype=self._dtype_of_feature_and_barcode_indices,
                    )  # create an empty array
                    int_pos = 0
                    for int_entry_of_axis_for_querying, a in zip(
                        l_int_entry_of_axis_for_querying,
                        l_arr_int_entry_of_axis_not_for_querying,
                    ):
                        n = len(a)
                        arr_int_entry_of_axis_for_querying[
                            int_pos : int_pos + n
                        ] = int_entry_of_axis_for_querying  # compose 'arr_int_entry_of_axis_for_querying'
                        int_pos += n  # update the current position
                    del (
                        l_int_entry_of_axis_for_querying,
                        l_arr_int_entry_of_axis_not_for_querying,
                    )  # delete intermediate objects

                    """ %% DENSE %% """
                    if flag_dense_ramtx_output:  # if dense output is present
                        za_mtx_dense.set_coordinate_selection(
                            (
                                arr_int_entry_of_axis_not_for_querying,
                                arr_int_entry_of_axis_for_querying,
                            )
                            if rtx_fork_safe.is_for_querying_features
                            else (
                                arr_int_entry_of_axis_for_querying,
                                arr_int_entry_of_axis_not_for_querying,
                            ),
                            arr_value,
                        )  # write dense zarr matrix

                    """ %% SPARSE %% """
                    if flag_sparse_ramtx_output:  # if sparse output is present
                        za_output_sparse[:int_num_records_written] = np.vstack(
                            (arr_int_entry_of_axis_not_for_querying, arr_value)
                        ).T  # save transformed data
                        za_output_sparse.resize(
                            int_num_records_written, 2
                        )  # resize the output Zarr object
                        pd.DataFrame(l_index).to_csv(
                            path_file_index_output_sparse,
                            header=None,
                            index=None,
                            sep="\t",
                        )  # write the index file

                    pipe_sender_result.send(
                        (
                            index_batch,
                            int_num_processed_records,
                            int_num_records_written,
                            path_folder_zarr_output_sparse,
                            path_file_index_output_sparse,
                        )
                    )  # send information about the output files
                # terminate spawned processes
                """ %% DENSE %% """
                if flag_dense_ramtx_output:  # if dense output is present
                    za_mtx_dense.terminate()
                rtx_fork_safe.terminate_spawned_processes()

            # initialize the progress bar
            l_mode_output = []
            if flag_dense_ramtx_output:
                l_mode_output.append("dense")
            if flag_sparse_ramtx_output:
                l_mode_output.append(mode_sparse)
            pbar = progress_bar(
                desc=f"{name_layer}/{rtx_fork_safe.mode} > {name_layer_new}/{', '.join( l_mode_output )}",
                total=rtx_fork_safe.get_total_num_records(
                    int_num_entries_for_each_weight_calculation_batch=self.int_num_entries_for_each_weight_calculation_batch,
                    flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=self.flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx,
                ),
            )
            """ %% SPARSE %% """
            if flag_sparse_ramtx_output:
                """create a worker process for off-laoding works (mostly file I/O) asynchronously so that main process can delegate works to the working processes without being blocked during file I/O."""

                def post_processing_sparse_matrix_output(pipe_input, pipe_output):
                    """# 2022-12-04 14:47:27
                    post-process sparse matrix output
                    """
                    # initialize
                    flag_is_destination_remote = is_remote_url(
                        path_folder_ramtx_sparse_mtx
                    )  # flag indicating whether a output destination is remotely located
                    path_folder_local_dest = (
                        f"{path_folder_temp}matrix.zarr/"
                        if flag_is_destination_remote
                        else path_folder_ramtx_sparse_mtx
                    )  # define a path to the local output folder, which is either final destionation (local output) or temporary destionation before being uploaded (remote output)

                    fs = FileSystemServer(
                        flag_spawn=flag_spawn
                    )  # initialize a filesystem server
                    fs.filesystem_operations(
                        "mkdir", path_folder_local_dest
                    )  # make the local output folder
                    # initialize zarr objects
                    za_mtx_sparse = ZarrServer(
                        path_folder_ramtx_sparse_mtx, mode="a", flag_spawn=flag_spawn
                    )  # use the same chunk size of the current RAMtx
                    za_mtx_sparse_index = ZarrServer(
                        f"{path_folder_ramtx_sparse}matrix.index.zarr",
                        mode="a",
                        flag_spawn=flag_spawn,
                    )  # use the same dtype and chunk size of the current RAMtx
                    int_num_chunks_written_to_ramtx = 0  # initialize the number of chunks written to ramtx object # the number of chunks already present in the output RAMtx zarr matrix object
                    int_len_matrix = 1  # default length # keep track the number of rows in the output sparse matrix in order to resize the matrix once the output has been written

                    # start processing
                    while True:
                        """receive inputs"""
                        ins = pipe_input.recv()
                        if ins is None:  # if None is received, exit
                            break
                        (
                            index_batch,
                            int_num_processed_records,
                            int_num_records_written,
                            path_folder_zarr_output,
                            path_file_index_output,
                        ) = ins  # parse inputs

                        """ post-process sparse matrix output """
                        # prepare
                        int_num_chunks_written_for_a_batch = int(
                            np.ceil(
                                int_num_records_written
                                / int_num_records_in_a_chunk_of_mtx_sparse
                            )
                        )  # retrieve the number of chunks that were written for a batch

                        # check size of Zarr matrix object, and increase the size if needed.
                        int_min_num_rows_required = (
                            int_num_chunks_written_to_ramtx
                            + int_num_chunks_written_for_a_batch
                        ) * int_num_records_in_a_chunk_of_mtx_sparse  # calculate the minimal number of rows required in the RAMtx Zarr matrix object
                        if (
                            za_mtx_sparse.shape[0] < int_min_num_rows_required
                        ):  # check whether the size of Zarr matrix is smaller than the minimum requirement
                            za_mtx_sparse.resize(
                                int_min_num_rows_required, 2
                            )  # resize the Zarr matrix so that data can be safely added to the matrix

                        # copy Zarr chunks to the sparse RAMtx Zarr matrix object folder
                        os.chdir(
                            path_folder_zarr_output
                        )  # to reduce the length of file path, change directory to the output folder before retrieving file paths of the chunks
                        for e in glob.glob(
                            "*.0"
                        ):  # to reduce the size of file paths returned by glob, use relative path to retrieve the list of chunk files of the Zarr matrix of the current batch
                            index_chunk = int(
                                e.split(".0", 1)[0]
                            )  # retrieve the integer index of the chunk
                            os.rename(
                                e,
                                path_folder_local_dest
                                + str(index_chunk + int_num_chunks_written_to_ramtx)
                                + ".0",
                            )  # simply rename the chunk to transfer stored values

                        # upload chunks to remote locations and delete local chunks
                        if flag_is_destination_remote:
                            # %% REMOTE %%
                            fs.filesystem_operations(
                                "cp",
                                path_folder_local_dest,
                                path_folder_ramtx_sparse,
                                flag_recursive=True,
                            )  # upload the processed chunks to the remote locations
                            fs.filesystem_operations(
                                "rm", path_folder_local_dest, flag_recursive=True
                            )  # delete the processed chunks
                            fs.filesystem_operations(
                                "mkdir", path_folder_local_dest
                            )  # re-create the local temporary output folder

                        # retrieve index data of the current batch
                        arr_index = pd.read_csv(
                            path_file_index_output, header=None, sep="\t"
                        ).values.astype(
                            int
                        )  # convert to integer dtype
                        arr_index[:, 1:] += (
                            int_num_chunks_written_to_ramtx
                            * int_num_records_in_a_chunk_of_mtx_sparse
                        )  # match the chunk boundary. if there are empty rows in the chunks currently written to ramtx, these empty rows will be considered as rows containing records, so that Zarr matrix written for a batch can be easily transferred by simply renaming the chunk files
                        za_mtx_sparse_index.set_orthogonal_selection(
                            arr_index[:, 0], arr_index[:, 1:]
                        )  # update the index of the entries of the current batch
                        int_len_matrix = arr_index[
                            -1, -1
                        ]  # update the number of rows in the output sparse matrix

                        # update the number of chunks written to RAMtx Zarr matrix object
                        int_num_chunks_written_to_ramtx += (
                            int_num_chunks_written_for_a_batch
                        )

                        # delete temporary files and folders
                        fs.filesystem_operations("rm", path_folder_zarr_output)
                        fs.filesystem_operations("rm", path_file_index_output)
                    """ send output and indicate the post-processing has been completed """
                    pipe_output.send(int_len_matrix)
                    # delete temporary folders
                    if (
                        flag_is_destination_remote
                    ):  # delete local destination folder only when the final destination folder is located remotely (when the final destination folder is located locally, the final destination folder is the 'path_folder_local_dest')
                        fs.filesystem_operations("rm", path_folder_local_dest)
                    # terminate the zarr servers
                    za_mtx_sparse.terminate()
                    za_mtx_sparse_index.terminate()
                    # terminate the file server
                    fs.terminate()
                    return  # exit

                # create pipes for communications
                (
                    pipe_sender_input_sparse_matrix_post_processing,
                    pipe_receiver_input_sparse_matrix_post_processing,
                ) = mp.Pipe()
                (
                    pipe_sender_output_sparse_matrix_post_processing,
                    pipe_receiver_output_sparse_matrix_post_processing,
                ) = mp.Pipe()
                # create and start a worker process for post-processing of the sparse matrix
                p_sparse_matrix_post_processing = mp.Process(
                    target=post_processing_sparse_matrix_output,
                    args=(
                        pipe_receiver_input_sparse_matrix_post_processing,
                        pipe_sender_output_sparse_matrix_post_processing,
                    ),
                )
                p_sparse_matrix_post_processing.start()  # start the process

            def post_process_batch(res):
                """# 2022-09-16 14:10:22"""
                # check whether the returned result was valid
                if res is None:
                    return
                # parse result
                (
                    index_batch,
                    int_num_processed_records,
                    int_num_records_written,
                    path_folder_zarr_output,
                    path_file_index_output,
                ) = res
                ns[
                    "int_num_records_written_to_ramtx"
                ] += int_num_records_written  # update the number of records written to the output RAMtx

                """ %% SPARSE %% """
                if flag_sparse_ramtx_output:  # if sparse output is present
                    """collect result of the current batch"""
                    while (
                        len(ns["l_res_sparse"]) < index_batch + 1 + 1
                    ):  # increase the length of ns[ 'l_res_sparse' ] until it can contain the result produced from the current batch. # add a padding (+1) to not raise indexError
                        ns["l_res_sparse"].append(
                            0
                        )  # not completed batch will be marked by 0
                    ns["l_res_sparse"][
                        index_batch
                    ] = res  # collect the result produced from the current batch

                    """ process results produced from batches in the order the batches were generated (in an ascending order of 'int_entry') """
                    while (
                        ns["l_res_sparse"][
                            ns["index_batch_waiting_to_be_written_sparse"]
                        ]
                        != 0
                    ):  # if the batch referenced by ns[ 'index_batch_waiting_to_be_written_sparse' ] has been completed
                        res_batch_for_post_processing = ns["l_res_sparse"][
                            ns["index_batch_waiting_to_be_written_sparse"]
                        ]  # retrieve 'res_batch' for post_processing
                        (
                            index_batch,
                            int_num_processed_records,
                            int_num_records_written,
                            path_folder_zarr_output,
                            path_file_index_output,
                        ) = res_batch_for_post_processing  # parse result
                        # if zero number of records were written, update the progress bar and continue to the next batch
                        if int_num_records_written == 0:
                            ns["l_res_sparse"][
                                ns["index_batch_waiting_to_be_written_sparse"]
                            ] = None  # remove the result from the list of batch outputs
                            ns[
                                "index_batch_waiting_to_be_written_sparse"
                            ] += 1  # start waiting for the next batch to be completed
                            pbar.update(
                                int_num_processed_records
                            )  # update the progress bar
                            continue

                        # send input to the worker for asynchronous post-processing of sparse-matrix
                        pipe_sender_input_sparse_matrix_post_processing.send(
                            res_batch_for_post_processing
                        )

                        ns["l_res_sparse"][
                            ns["index_batch_waiting_to_be_written_sparse"]
                        ] = None  # remove the result from the list of batch outputs
                        ns[
                            "index_batch_waiting_to_be_written_sparse"
                        ] += 1  # start waiting for the next batch to be completed
                        pbar.update(
                            int_num_processed_records
                        )  # update the progress bar
                os.chdir(
                    self.path_folder_temp
                )  # change path to root temporary folder before deleting the current temp folder (to avoid deleting the working directory)

            # transform the values of the RAMtx using multiple processes
            bk.Multiprocessing_Batch_Generator_and_Workers(
                rtx_fork_safe.batch_generator(
                    ax.filter,
                    int_num_entries_for_each_weight_calculation_batch=self.int_num_entries_for_each_weight_calculation_batch,
                    int_total_weight_for_each_batch=self.int_total_weight_for_each_batch,
                    flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=self.flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx,
                ),
                process_batch,
                post_process_batch=post_process_batch,
                int_num_threads=int_num_threads,
                int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
            )  # create batch considering chunk boundaries # return batch index to allow combining sparse matrix in an ascending order.
            pbar.close()  # close the progress bar

            """ export ramtx settings """
            """ %% DENSE %% """
            if flag_dense_ramtx_output:  # if dense output is present
                fs.filesystem_operations(
                    "rm", path_file_lock_mtx_dense
                )  # delete file system locks
                # save a zarr metadata
                zms.set_metadata(
                    path_folder_ramtx_dense,
                    "dict_metadata",
                    {
                        "mode": "dense",
                        "str_completed_time": bk.TIME_GET_timestamp(True),
                        "int_num_features": int_num_features,
                        "int_num_barcodes": int_num_barcodes,
                        "int_num_records": ns["int_num_records_written_to_ramtx"],
                        "version": _version_,
                    },
                )
                # terminate the zarr server
                za_mtx_dense.terminate()

            """ %% SPARSE %% """
            if flag_sparse_ramtx_output:  # if sparse output is present
                # save a metadata
                zms.set_metadata(
                    path_folder_ramtx_sparse,
                    "dict_metadata",
                    {
                        "mode": mode_sparse,
                        "flag_ramtx_sorted_by_id_feature": rtx.is_for_querying_features,
                        "str_completed_time": bk.TIME_GET_timestamp(True),
                        "int_num_features": int_num_features,
                        "int_num_barcodes": int_num_barcodes,
                        "int_num_records": ns["int_num_records_written_to_ramtx"],
                        "version": _version_,
                    },
                )
                # retrieve result from the worker process
                pipe_sender_input_sparse_matrix_post_processing.send(
                    None
                )  # indicate all work has been completed
                int_len_matrix = (
                    pipe_receiver_output_sparse_matrix_post_processing.recv()
                )  # receive the length of the matrix
                p_sparse_matrix_post_processing.join()  # dismiss worker
                # resize the za_mtx_sparse matrix if its length is larger than 'int_len_matrix'
                if za_mtx_sparse.shape[0] > int_len_matrix:
                    za_mtx_sparse.resize(
                        int_len_matrix, 2
                    )  # resize the Zarr matrix to according to the actual number of rows in the matrix

                # terminate the zarr servers
                za_mtx_sparse.terminate()
                za_mtx_sparse_index.terminate()

            # remove temp folder once all operations have been completed
            fs.filesystem_operations("rm", path_folder_temp)

            # terminate spawned processes
            rtx_fork_safe.terminate_spawned_processes()
            fs.terminate()  # terminate the file server
            zms.terminate()  # terminate the zarr metadata server
            return  # exit
            # END of RAMtx_Apply function

        # initialize the list arguments for running multiple processes
        l_args = []

        """
        pre-process 'mode_instructions'
        """

        # handle the given argument
        # find the element with mimimum nested list depth, and if it is less than 2, wrap the 'mode_instructions' in a list until the minimum nested list depth becomes 2
        def __find_min_depth(l, current_depth=0):
            """# 2022-07-31 15:56:55
            breadth search for finding the min depth of a given nested list
            """
            if isinstance(l, (str, dict)):
                return current_depth
            else:
                return min(
                    __find_min_depth(e, current_depth=current_depth + 1) for e in l
                )

        for _ in range(2 - __find_min_depth(mode_instructions)):
            mode_instructions = [mode_instructions]
        # compose default setting
        dict_setting_default = {
            "dtype_of_row_and_col_indices": dtype_of_row_and_col_indices,
            "dtype_of_value": dtype_of_value,
            "int_num_of_records_in_a_chunk_zarr_matrix": int_num_of_records_in_a_chunk_zarr_matrix,
            "int_num_of_entries_in_a_chunk_zarr_matrix_index": int_num_of_entries_in_a_chunk_zarr_matrix_index,
            "chunks_dense": chunks_dense,
            "dtype_dense_mtx": dtype_dense_mtx,
            "dtype_sparse_mtx": dtype_sparse_mtx,
            "dtype_sparse_mtx_index": dtype_sparse_mtx_index,
        }
        # { 'dense', 'dense_for_querying_barcodes', 'dense_for_querying_features', 'sparse_for_querying_barcodes', 'sparse_for_querying_features' }
        set_modes_sink_valid = {
            "dense",
            "sparse_for_querying_barcodes",
            "sparse_for_querying_features",
        }
        set_modes_sink = (
            set(self.layer.modes) if flag_update_a_layer else set()
        )  # retrieve the ramtx modes in the output (sink) layer (assumes a data sink layer (that is not data source layer) does not contain any ramtx objects). # to avoid overwriting
        set_modes_sink.update(
            layer_new.modes
        )  # update available modes in the output layer
        for an_instruction in mode_instructions:  # first instructions takes priority
            """
            pre-process each instruction
            """
            # parse 'dict_setting_of_an_instruction'
            dict_setting_of_an_instruction = (
                dict_setting_default  # use the default setting by default
            )
            if isinstance(
                an_instruction[-1], dict
            ):  # if a specific 'dict_setting_of_an_instruction' was given
                dict_setting_of_an_instruction = (
                    dict_setting_default | an_instruction[-1]
                )
                an_instruction = an_instruction[
                    :-1
                ]  # remove 'dict_setting_of_an_instruction' from 'an_instruction'
                if len(an_instruction) < 1:
                    logger.error(
                        f"an incomplete instruction was given with only {dict_setting_of_an_instruction = }, which will be ignored."
                    )
                    continue

            # parse the rest of the instruction
            # if the 'ramtx_mode_sink' has not been set, 'ramtx_mode_source' will be used as the mode of the ramtx sink, too.
            if len(an_instruction) == 1:
                an_instruction = an_instruction * 2
            (
                ramtx_mode_source,
                l_ramtx_mode_sink,
            ) = an_instruction  # parse an instruction
            # if 'l_ramtx_mode_sink' is a single 'ramtx_mode_sink', wrap the entry in a list
            if isinstance(l_ramtx_mode_sink, str):
                l_ramtx_mode_sink = [l_ramtx_mode_sink]
            # if 'ramtx_mode_source' does not exist in the current layer, ignore the current instruction
            if ramtx_mode_source not in self.layer:
                continue
            # compose a valid set of 'ramtx_mode_sink'
            set_ramtx_mode_sink = (
                set(
                    "dense" if "dense" in e else e
                    for e in list(e.lower() for e in l_ramtx_mode_sink)
                )
                .intersection(set_modes_sink_valid)
                .difference(set_modes_sink)
            )  # for each given valid 'ramtx_mode_sink' # if 'ramtx_mode_sink' already exists in the output layer (or will exists after running previous instructions), ignore 'ramtx_mode_sink'
            # if there is no valid ramtx sink modes, ignore the instruction
            if len(set_ramtx_mode_sink) == 0:
                continue

            """
            compose process
            """
            flag_dense_ramtx_output, flag_sparse_ramtx_output = False, False
            if not "dense" in ramtx_mode_source:  # sparse source
                if ramtx_mode_source in set_ramtx_mode_sink:  # sparse sink presents
                    flag_sparse_ramtx_output = True
                    set_modes_sink.add(
                        ramtx_mode_source
                    )  # update written (or will be written) sink ramtx modes
                if "dense" in set_ramtx_mode_sink:  # dense sink presents
                    flag_dense_ramtx_output = True
                    set_modes_sink.add(
                        "dense"
                    )  # update written (or will be written) sink ramtx modes

                flag_source_querying_by_feature = (
                    "features" in ramtx_mode_source
                )  # retrieve a flag indicating whether the source can be queried by features
                # add a process if valid output exists
                if flag_sparse_ramtx_output or flag_dense_ramtx_output:
                    l_args.append(
                        (
                            self,
                            self.layer.get_ramtx(
                                flag_source_querying_by_feature, flag_prefer_dense=False
                            ),
                            func_ft if flag_source_querying_by_feature else func_bc,
                            flag_dense_ramtx_output,
                            flag_sparse_ramtx_output,
                            int_num_threads,
                            dict_setting_of_an_instruction,
                        )
                    )  # add process based on which axis will be queried for source ramtx # prefer sparse RAMtx over dense matrix when selecting matrix
            else:  # dense source
                set_modes_sink.update(
                    set_ramtx_mode_sink
                )  # update written (or will be written) sink ramtx modes. dense source can write all sink modes
                if "dense" in set_ramtx_mode_sink:  # dense sink presents
                    flag_dense_ramtx_output = True
                flag_querying_features = (
                    self.layer["dense"].is_for_querying_features
                    if ramtx_mode_source == "dense"
                    else "features" in ramtx_mode_source
                )  # retrieve a flag for querying with features
                if (
                    "sparse_for_querying_barcodes" in set_ramtx_mode_sink
                    and "sparse_for_querying_features" in set_ramtx_mode_sink
                ):  # if both sparse sink modes are present, run two processes, and add dense sink to one of the processes based on the given preference
                    l_args.append(
                        (
                            self,
                            self.layer["dense_for_querying_barcodes"],
                            func_bc,
                            flag_dense_ramtx_output and (not flag_querying_features),
                            True,
                            int_num_threads,
                            dict_setting_of_an_instruction,
                        )
                    )  # add a process for querying barcodes
                    l_args.append(
                        (
                            self,
                            self.layer["dense_for_querying_features"],
                            func_ft,
                            flag_dense_ramtx_output and flag_querying_features,
                            True,
                            int_num_threads,
                            dict_setting_of_an_instruction,
                        )
                    )  # add a process for querying features
                elif (
                    "sparse_for_querying_barcodes" in set_ramtx_mode_sink
                ):  # if only a single sparse ramtx (barcodes-indexed) sink is present
                    l_args.append(
                        (
                            self,
                            self.layer["dense_for_querying_barcodes"],
                            func_bc,
                            flag_dense_ramtx_output,
                            True,
                            int_num_threads,
                            dict_setting_of_an_instruction,
                        )
                    )  # add a process for querying barcodes
                elif (
                    "sparse_for_querying_features" in set_ramtx_mode_sink
                ):  # if only a single sparse ramtx (features-indexed) sink is present
                    l_args.append(
                        (
                            self,
                            self.layer["dense_for_querying_features"],
                            func_ft,
                            flag_dense_ramtx_output,
                            True,
                            int_num_threads,
                            dict_setting_of_an_instruction,
                        )
                    )  # add a process for querying features
                elif (
                    flag_dense_ramtx_output
                ):  # if only dense sink present, use the axis based on the given preference
                    l_args.append(
                        (
                            self,
                            self.layer[
                                f"dense_for_querying_{'features' if flag_querying_features else 'barcodes'}"
                            ],
                            func_ft if flag_querying_features else func_bc,
                            True,
                            False,
                            int_num_threads,
                            dict_setting_of_an_instruction,
                        )
                    )  # add a process for querying features

        """
        Run Processes
        """
        if len(l_args) == 0:
            if self.verbose:
                logger.info(
                    "[RamData.apply] no operation was performed (output already exists)."
                )
            return

        # logger.info( f"{l_args = }" )

        # since a zarr object will be modified by multiple processes, setting 'numcodecs.blosc.use_threads' to False as recommended by the zarr documentation
        zarr_start_multiprocessing_write()

        if (
            self.contains_remote and name_layer not in self.layers_excluding_components
        ):  #  or is_remote_url( path_folder_ramdata_output )
            # if current RamData contains data hosted remotely and current layer consists of components (which indicates that zarr objects from remote locations will be used), avoid multi-processing due to current lack of support for multi-processing on Zarr HTTPStore. Also, when output folder is a remote location, avoid multiprocessing 'RAMtx_Apply' since s3fs appears to be not fork-safe
            for args in l_args:
                RAMtx_Apply(*args)
        else:
            # run multiple processes
            l_p = list(mp.Process(target=RAMtx_Apply, args=args) for args in l_args)
            for p in l_p:
                p.start()
            for p in l_p:
                p.join()

        # revert to the original the setting
        zarr_end_multiprocessing_write()

        if self.use_locking:  # %% FILE LOCKING %%
            # locks of the input and output layers
            self._zsls.release_lock(
                path_lock_layer_input
            )  # release locks for the input layer
            self._zsls.release_lock(
                path_lock_layer_output
            )  # release locks for the output layer

        """
        update the metadata
        """
        # update metadata of the output layer
        layer_new.update_metadata(
            l_mode_to_be_added=list(set_modes_sink)
            + (
                ["dense_for_querying_barcodes", "dense_for_querying_features"]
                if "dense" in set_modes_sink
                else []
            )
        )

        # survey weights
        if flag_survey_weights:
            layer_new._load_ramtx_objects()  # load ramtx objects for the output layer
            for mode in layer_new.modes:  # for each available RAMtx object
                layer_new[
                    mode
                ].survey_number_of_records_for_each_entry()  # survey weights for the current RAMtx object
        if (
            flag_update_a_layer
        ):  # if the current layer has been updated, reload the RAMtx objects
            # reload the layer
            self.layer = None
            self.layer = name_layer

        # update metadata of current RamData
        # update 'layers' if the layer has been saved in the current RamData object (or the mask of the current RamData object)
        if flag_new_layer_added_to_the_current_ramdata and not flag_update_a_layer:
            self._add_layer(
                name_layer=name_layer_new,
                dict_metadata_description=dict_metadata_description,
            )  # add layer to the current ramdata

        # report results
        if self.verbose:
            logger.info(
                f"[RamData.apply] apply operation {name_layer} > {name_layer_new} has been completed"
            )

    """ </CORE METHODS> """

    def subset(
        self,
        path_folder_ramdata_output,
        l_name_layer: list = [],
        dict_mode_instructions: dict = dict(),
        int_num_threads=None,
        flag_survey_weights=False,
        l_name_col_bc: Union[None, list] = None,
        l_name_col_ft: Union[None, list] = None,
        set_type_model: Union[None, set] = None,
        set_id_model: Union[None, set] = None,
        **kwargs,
    ):
        """# 2023-02-22 21:51:33
        this function will create a new RamData object on disk by creating a subset of the current RamData according to the current set of barcode and features axis filters. the following components will be subsetted.
            - Axis
                 - Metadata
                 - String representations
            - Layer

        currently, models will not be subsetted, and should be created anew from the resulting RamData.

        =========
        inputs
        =========
        'path_folder_ramdata_output' : The directory of the RamData object that will contain a subset of the barcodes/features of the current RamData.
        'l_name_layer' : the list of name_layers to subset and transfer to the new RamData object
        'int_num_threads' : the number of CPUs to use. by default, the number of CPUs set by the RamData attribute 'int_num_cpus' will be used.
        'dict_mode_instructions' : a dictionary with key = name_layer, value = 'mode_instructions' arguments for 'RamData.apply' method
        'flag_survey_weights' : survey the weights of the output RAMtx objects of the output layers

        'l_name_col_bc' : the list of names of columns of the metadata of the barcode axis to save. if None is given, all columns of the metadata of 'barcode' axis will be saved
        'l_name_col_ft' : the list of names of columns of the metadata of the feature axis to save. if None is given, all columns of the metadata of 'feature' axis will be saved


        === models ===
        Currently, only KNN-index models are supported.

        set_id_model : Union[ None, set ] = None # a set containing id_model of the models to save, which is composed by f"{name_model}|{type_model}". By default, copying all the models available for the current RamData.
        set_type_model : Union[ None, set ] = None # a set containing type_model to save. by default, using all compatible model types
        """
        """ handle inputs """
        # internal parameters
        set_type_model_valid = {
            "knnindex",
            f"deep_learning.keras.classifier",
            f"deep_learning.keras.embedder",
            "ipca",
        }  # mostly the models that based on data of the axis metadata and does not rely on the data from layer, where the model, in a subset, it can be used natively.

        # handle inputs
        set_type_model = (
            set_type_model.intersection(set_type_model_valid)
            if isinstance(set_type_model, set)
            else set_type_model_valid
        )  # retrieve 'set_type_model' containing valid type_models

        dict_metadata_models_excluding_components = self.models_excluding_components
        # set default value of 'set_id_model'
        if not isinstance(set_id_model, set):
            set_id_model = set(
                dict_metadata_models_excluding_components
            )  # retrieve a set of valid 'id_model'
        set_id_model = set(
            e
            for e in set_id_model
            if e.rsplit("|", 1)[1] in set_type_model
            and e in dict_metadata_models_excluding_components
            and dict_metadata_models_excluding_components[e][
                "identifier_of_the_ramdata_of_origin"
            ]
            == self.identifier
        )  # exclude the id_model with invalid type_model, included only id_model in 'models_excluding_components', and belonging to the current ramdata

        # check invalid input
        if path_folder_ramdata_output == self._path_folder_ramdata:
            if self.verbose:
                logger.info(
                    f"the output RamData object directory is exactly same that of the current RamData object, exiting"
                )
        # create the RamData output folder
        filesystem_operations("mkdir", path_folder_ramdata_output, exist_ok=True)

        # retrieve valid set of name_layer
        set_name_layer = self.layers.intersection(l_name_layer)

        # initialize and destroy the view after subsetting
        with self as view:  # load 'dict_change' for coordinate conversion according to the given filters, creating the view of the RamData
            """RamDataAxis"""
            # copy axes and associated metadata
            view.bc.save(path_folder_ramdata_output, l_name_col=l_name_col_bc)
            view.ft.save(path_folder_ramdata_output, l_name_col=l_name_col_ft)

            """ RamDataLayer """
            for name_layer in set_name_layer:  # for each valid name_layer
                # skip if instructions are not available
                if name_layer not in dict_mode_instructions:
                    continue

                # output a subset of the layer using the instructions
                view.apply(
                    name_layer,
                    name_layer_new=None,
                    func="ident",
                    mode_instructions=dict_mode_instructions[
                        name_layer
                    ],  # use mode_instructions of the given layer
                    path_folder_ramdata_output=path_folder_ramdata_output,
                    int_num_threads=int_num_threads,
                    flag_survey_weights=flag_survey_weights,
                    **kwargs,
                )  # flag_dtype_output = None : use the same dtype as the input RAMtx object

        # compose metadata
        root = zarr.group(path_folder_ramdata_output)
        dict_metadata = deepcopy(self.metadata)  # get metadata of the current RamData
        # update the metadata
        dict_metadata.update(
            {
                "path_folder_mtx_10x_input": None,
                "str_completed_time": bk.TIME_GET_timestamp(True),
                "int_num_features": self.ft.meta.n_rows,
                "int_num_barcodes": self.bc.meta.n_rows,
                "layers": dict((name_layer, dict()) for name_layer in set_name_layer),
                "models": dict(),
                "version": _version_,
                "identifier": bk.UUID(),
            }
        )
        root.attrs["dict_metadata"] = dict_metadata  # write the metadata
        # open the destination RamData
        ram_subset = RamData(path_folder_ramdata_output)

        """ copy (re-build) models """
        # copy models
        for id_model in set_id_model:  # for each valid model
            name_model, type_model = id_model.rsplit("|", 1)

            # load the model
            model = self.load_model(
                name_model=name_model,
                type_model=type_model,
            )
            """ prepare """
            if (
                "identifier" in model
            ):  # change identifier to the that of the destination RamData
                model["identifier"] = ram_subset.identifier

            if "flag_axis_is_barcode" in model:  # load axis object
                # retrieve axes object
                ax, ax_features, ax_subset, ax_features_subset = (
                    (self.bc, self.ft, ram_subset.bc, ram_subset.ft)
                    if model["flag_axis_is_barcode"]
                    else (self.ft, self.bc, ram_subset.ft, ram_subset.bc)
                )  # retrieve axes of the source and destination ramdata objects

            if "filter" in model:  # load filter for building the model.
                # build the filter for the destination RamData object
                if (
                    ax.filter is None
                ):  # if all entries are active in the source RamData, all entries in the destination RamData will be used.
                    ba_subset = model["filter"]  # filter of the destination RamData
                else:
                    ba_subset = ax_subset.none()
                    for index_subset, index in enumerate(
                        BA.find(ax.filter)
                    ):  # retrieve indices of input and output ramdata objects
                        if model["filter"][index]:
                            ba_subset[index_subset] = True
                # set the filter of the output object
                ax_subset.filter = ba_subset

            if (
                "filter_of_axis_features" in model
            ):  # load filter of the axis representing features for building the model.
                # build the filter for the destination RamData object
                if (
                    ax_features.filter is None
                ):  # if all entries are active in the source RamData, all entries in the destination RamData will be used.
                    ba_features_subset = model[
                        "filter_of_axis_features"
                    ]  # filter of the destination RamData
                else:
                    ba_features_subset = ax_features_subset.none()
                    for index_subset, index in enumerate(
                        BA.find(ax_features.filter)
                    ):  # retrieve indices of input and output ramdata objects
                        if model["filter_of_axis_features"][index]:
                            ba_features_subset[index_subset] = True
                # set the filter of the output object
                ax_features_subset.filter = ba_features_subset

            """ re-build models """
            if type_model == "knnindex":
                """re-build 'knnindex'"""
                # check requirements
                # if required columns are absent, skip re-building the model
                if not (
                    model["name_col_x"] in ax_subset.columns
                    and (
                        model["name_col_filter_for_collecting_neighbors"] is None
                        or model["name_col_filter_for_collecting_neighbors"]
                        in ax_subset.columns
                    )
                ):
                    if self.verbose:
                        logger.info(
                            f"required columns for exporting '{id_model}' model are absent in the destination RamData. The model will be skipped."
                        )
                    continue

                ram_subset.train_knn(
                    name_model=name_model,
                    name_col_x=model["name_col_x"],
                    axis="barcodes" if model["flag_axis_is_barcode"] else "features",
                    int_num_components_x=model["int_num_components_x"],
                    n_neighbors=model["knnindex"].n_neighbors,
                    name_col_filter_for_collecting_neighbors=model[
                        "name_col_filter_for_collecting_neighbors"
                    ],
                    int_num_nearest_neighbors_to_collect=model[
                        "int_num_nearest_neighbors_to_collect"
                    ],
                )
            elif type_model in {
                "deep_learning.keras.classifier",
                "deep_learning.keras.embedder",
            }:
                """export deep learning models"""
                # no requirements for exporting deep learning models

                # modify 'filter' attribute of the model
                model["filter"] = ba_subset

                # load the model
                ram_subset.save_model(
                    model,
                    name_model=name_model,
                    type_model=type_model,
                )
            elif type_model == "ipca":
                """export deep learning models"""
                # currently, for 'ipca' model to be saved to the destination RamData, all the entries of the axis representing features should exist in the axis of the destination RamData.
                if (
                    model["filter_of_axis_features"].count()
                    != ba_features_subset.count()
                ):  # the number of entries in the filter saved with model should be same as the filter representing the subset of the filter saved with the model, meaning that all entries should exist in the axis of the destination RamData
                    continue

                # modify 'filter' attribute of the model
                model["filter_of_axis_features"] = ba_features_subset

                # load the model
                ram_subset.save_model(
                    model,
                    name_model=name_model,
                    type_model=type_model,
                )

    def normalize(
        self,
        name_layer="raw",
        name_layer_new="normalized",
        name_col_total_count="raw_sum",
        int_total_count_target=10000,
        mode_instructions=[
            ["sparse_for_querying_features", "sparse_for_querying_features"],
            ["sparse_for_querying_barcodes", "sparse_for_querying_barcodes"],
        ],
        int_num_threads=None,
        **kwargs,
    ):
        """# 2022-07-06 23:58:15
        this function perform normalization of a given data and will create a new data in the current RamData object.

        =========
        inputs
        =========

        'name_layer' : name of input data
        'name_layer_new' : name of the output (normalized) data
        'name_col_total_count' : name of column of barcode metadata (ZarrDataFrame) to use as total counts of barcodes
        'int_total_count_target' : the target total count. the count data will be normalized according to the total counts of barcodes so that the total counts of each barcode after normalization becomes 'int_total_count_target'.
        'mode_instructions' : please refer to the RamData.apply method
        'int_num_threads' : the number of CPUs to use. by default, the number of CPUs set by the RamData attribute 'int_num_cpus' will be used.

        ** kwargs : arguments for 'RamData.apply' method
        """
        # check validity of inputs
        if (
            name_col_total_count not in self.bc.meta
        ):  # 'name_col_total_count' column should be available in the metadata
            if self.verbose:
                logger.info(
                    f"[RamData.normalize] 'name_col_total_count' '{name_col_total_count}' does not exist in the 'barcodes' metadata, exiting"
                )
            return

        # load total count data
        flag_name_col_total_count_already_loaded = (
            name_col_total_count in self.bc.meta.dict
        )  # a flag indicating that the total count data of barcodes has been already loaded
        if (
            not flag_name_col_total_count_already_loaded
        ):  # load count data of barcodes in memory
            self.bc.meta.load_as_dict(name_col_total_count)
        dict_count = self.bc.meta.dict[
            name_col_total_count
        ]  # retrieve total count data as a dictionary

        # load layer
        self.layer = name_layer

        # define functions for normalization
        def func_norm_barcode_indexed(
            self,
            int_entry_of_axis_for_querying,
            arr_int_entries_of_axis_not_for_querying,
            arr_value,
        ):
            """# 2022-07-06 23:58:27"""
            return (
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                (
                    arr_value
                    / dict_count[int_entry_of_axis_for_querying]
                    * int_total_count_target
                ),
            )  # normalize count data of a single barcode

        def func_norm_feature_indexed(
            self,
            int_entry_of_axis_for_querying,
            arr_int_entries_of_axis_not_for_querying,
            arr_value,
        ):  # normalize count data of a single feature containing (possibly) multiple barcodes
            """# 2022-07-06 23:58:38"""
            # perform normalization in-place
            for i, e in enumerate(
                arr_int_entries_of_axis_not_for_querying.astype(int)
            ):  # iterate through barcodes
                arr_value[i] = (
                    arr_value[i] / dict_count[e]
                )  # perform normalization of count data for each barcode
            arr_value *= int_total_count_target
            return (
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            )

        """ normalize the RAMtx matrices """
        self.apply(
            name_layer,
            name_layer_new,
            func=(func_norm_barcode_indexed, func_norm_feature_indexed),
            int_num_threads=int_num_threads,
            mode_instructions=mode_instructions,
            **kwargs,
        )  # flag_dtype_output = None : use the same dtype as the input RAMtx object

        if (
            not flag_name_col_total_count_already_loaded
        ):  # unload count data of barcodes from memory if the count data was not loaded before calling this method
            del self.bc.meta.dict[name_col_total_count]

    def scale(
        self,
        name_layer="normalized_log1p",
        name_layer_new="normalized_log1p_scaled",
        name_col_variance: Union[str, None] = "normalized_log1p_variance",
        max_value: Union[float, None] = 10,
        mode_instructions=[
            ["sparse_for_querying_features", "sparse_for_querying_features"],
            ["sparse_for_querying_barcodes", "sparse_for_querying_barcodes"],
        ],
        int_num_threads=None,
        **kwargs,
    ):
        """# 2022-11-24 01:35:09
        current implementation only allows output values to be not zero-centered. the zero-value will remain zero, while Z-scores of the non-zero values will be increased by Z-score of zero values, enabling processing of sparse count data

        'name_layer' : the name of the data source layer
        'name_layer_new' : the name of the data sink layer (new layer)
        'name_col_variance' : name of feature metadata containing variance informatin
        name_col_variance : Union[ str, None ] # name of feature metadata containing variance information. if None is given, does not divide input values by standard deviation of the feature
        max_value : Union[ float, None ] # clip values larger than 'max_value' to 'max_value'. if None is given, does not cap at max value
        'mode_instructions' : please refer to the RamData.apply method
        'int_num_threads' : the number of CPUs to use. by default, the number of CPUs set by the RamData attribute 'int_num_cpus' will be used.

        ** kwargs : arguments for 'RamData.apply' method
        """
        # retrieve flags
        flag_cap_value = max_value is not None
        flag_divide_by_sd = (
            name_col_variance is not None and name_col_variance in self.ft.columns
        )  # the 'name_col_variance' column name should be present in the metadata zdf.

        # load variance data
        if flag_divide_by_sd:
            """
            %% load variance data %%
            """
            # check validity of inputs
            # column names should be available in the metadata
            if (
                name_col_variance not in self.ft.meta
            ):  # 'name_col_variance' column should be available in the metadata
                if self.verbose:
                    logger.info(
                        f"[RamData.scale] 'name_col_variance' '{name_col_total_count}' does not exist in the 'barcodes' metadata, exiting"
                    )
                return

            # load feature data
            # retrieve flag indicating whether the data has been already loaded
            flag_name_col_variance_already_loaded = (
                name_col_variance in self.ft.meta.dict
            )
            if not flag_name_col_variance_already_loaded:  # load data in memory
                self.ft.meta.load_as_dict(name_col_variance)
            # retrieve data as a dictionary
            dict_variance = self.ft.meta.dict[name_col_variance]

        # load layer
        self.layer = name_layer

        # define functions for scaling
        def func_feature_indexed(
            self,
            int_entry_of_axis_for_querying,
            arr_int_entries_of_axis_not_for_querying,
            arr_value,
        ):
            """# 2022-07-27 14:32:21"""
            if flag_divide_by_sd:
                """
                %% divide by standard deviation (SD) %%
                """
                float_std = (
                    dict_variance[int_entry_of_axis_for_querying] ** 0.5
                )  # retrieve standard deviation from the variance
                if (
                    float_std != 0
                ):  # skip division when standard deviation is equal to or below zero (all the data values should be zero)
                    arr_value /= float_std  # scale count data using the standard deviation (in-place)
            """
            %% cap exceptionally large values %%
            """
            if flag_cap_value:
                arr_value[arr_value > max_value] = max_value
            return (
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            )  # return scaled data

        def func_barcode_indexed(
            self,
            int_entry_of_axis_for_querying,
            arr_int_entries_of_axis_not_for_querying,
            arr_value,
        ):  # normalize count data of a single barcode containing (likely) multiple features
            """# 2022-07-27 16:32:21"""
            # perform scaling in-place to reduce memory consumption
            if flag_divide_by_sd:
                """
                %% divide by standard deviation (SD) %%
                """
                for i, e in enumerate(
                    arr_int_entries_of_axis_not_for_querying.astype(int)
                ):  # iterate through barcodes
                    float_var = dict_variance[e]  # retrieve variance
                    if (
                        float_var != 0
                    ):  # if standard deviation is not available, use the data as-is
                        arr_value[i] = (
                            arr_value[i] / float_var**0.5
                        )  # retrieve standard deviation of the current feature from the variance # perform scaling of data for each feature
            """
            %% cap exceptionally large values %%
            """
            if flag_cap_value:
                arr_value[arr_value > max_value] = max_value
            return (
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            )  # return scaled data

        """ process the RAMtx matrices """
        self.apply(
            name_layer,
            name_layer_new,
            func=(func_barcode_indexed, func_feature_indexed),
            int_num_threads=int_num_threads,
            mode_instructions=mode_instructions,
            **kwargs,
        )  # flag_dtype_output = None : use the same dtype as the input RAMtx object

        # unload variance data
        if flag_divide_by_sd:
            if not flag_name_col_variance_already_loaded:
                del self.ft.meta.dict[name_col_variance]

    def identify_highly_variable_features(
        self,
        name_layer: str,
        int_num_highly_variable_features: Union[int, None] = 3500,
        float_min_mean: float = 0.01,
        float_min_variance: float = 0.01,
        str_suffix_summarized_metrics: str = "",
        str_suffix_mean_var_relationsip: str = "",
        name_col_filter: Union[str, None] = None,
        name_col_batch: Union[str, None] = None,
        int_index_secondary: Union[
            int, None
        ] = None,  # the secondary index of the columns
        flag_load_filter: bool = True,
        flag_show_graph: bool = True,
    ):
        """# 2023-05-01 11:29:24
        identify highly variable features
        learns mean-variable relationship from the given data, and calculate residual variance to identify highly variable features.

        int_num_highly_variable_features : Union[ int, None ] = 3500, # number of highly variable features to select. if None is given. a threshold for the selection of highly variable features will be set automatically to '0'.
        float_min_mean : float = 0.01, # minimum mean expression for selecting highly variable features
        float_min_variance : float = 0.01, # minimum variance of expression for selecting highly variable features
        str_suffix_summarized_metrics : str = '', # suffix of the new columns of the 'feature' axis that will contain summarized metrics of the features (mean, variance). [Important] when the barcode selection is changed, 'str_suffix_summarized_metrics' should be also changed to recalculate mean and variance of each feature.
        str_suffix_mean_var_relationsip : str = '', # suffix of the new columns of the 'feature' axis that will contain metrics from the learned mean-variance relationship. [Important] when the feature selection is changed, 'str_suffix_mean_var_relationsip' should be also changed to relearn mean-variance relationships of the selected features.
        name_col_filter : Union[ str, None ] = None, # the name of column that will contain a feature/barcode filter containing selected highly variable features (and barcode filter for cells that have non-zero expression values for the selected list of highly-variable features)
        name_col_batch : Union[ str, None ] = None, # the name of the column containing batch information. if None is given, all selected barcodes will be treated as a single batch.
        int_index_secondary : Union[ int, None ] = None, # the secondary index of the columns
        flag_load_filter : bool = True, # if True, load the filter of the column name 'name_col_filter' after the analysis has been completed.
        flag_show_graph : bool = True, # show graphs
        ==========
        returns
        ==========

        new columns will be added to self.ft.meta metadata
        """
        """
        prepare
        """
        # handle invalid inputs
        if name_col_batch is not None:
            if (
                name_col_batch not in self.bc.columns
            ):  # if 'name_col_batch' does not exist
                name_col_batch = None

        # retrieve axis object
        ax, ax_not_for_querying = self.ft, self.bc
        # retrieve metadata object
        zdf_meta = ax.meta
        # check whether the output is already available, and if exist, exit
        if (
            name_col_filter is not None and name_col_filter in ax.meta
        ):  # if the output already exists, load the filter (if relevant setting is on) and exit
            if flag_load_filter:  # load filter according to the filter
                ax.change_filter(name_col_filter)
            return

        if (
            name_col_batch is not None and name_col_batch in ax_not_for_querying.meta
        ):  # if 'name_col_batch' is a valid column
            """
            # %% BATCH-AWARE Highly variable gene detection
            identify highly variable genes using the batch information.
            """
            """
            (1) Calculate metrics for identification of highly variable features
            """

            # retrieve counts for each batch (for initialization of arrays)
            dict_batch_to_count = ax_not_for_querying.meta.count_category(
                name_col_batch, flag_use_integer_representation_of_category=True
            )  # use integer representations
            l_name_batch = ax_not_for_querying.meta.get_categories(
                name_col_batch
            )  # retrieve the names of the batches
            int_num_batches = len(l_name_batch)

            # retrieve batch information of barcodes
            ax_not_for_querying.meta.load_as_dict(
                name_col_batch, flag_retrieve_categorical_data_as_integers=True
            )  # use integer representations
            dict_batch = ax_not_for_querying.meta.dict.pop(name_col_batch)
            l_batch_active = (
                list(set(dict_batch[k] for k in dict_batch))
                if isinstance(dict_batch, dict)
                else np.unique(dict_batch)
            )  # retrieve the list of active batches

            # initialize output columns
            name_col_sum = f"sum__{name_col_batch}{str_suffix_summarized_metrics}"
            name_col_num_nonzero_values = (
                f"num_nonzero_values__{name_col_batch}{str_suffix_summarized_metrics}"
            )
            name_col_mean = f"mean__{name_col_batch}{str_suffix_summarized_metrics}"
            name_col_deviation = (
                f"deviation__{name_col_batch}{str_suffix_summarized_metrics}"
            )
            name_col_variance = (
                f"variance__{name_col_batch}{str_suffix_summarized_metrics}"
            )
            name_col_ratio_for_selection = f"_float_ratio_of_variance_to_expected_variance_from_mean__{name_col_batch}{str_suffix_summarized_metrics}"
            name_col_diff_for_selection = f"_float_diff_of_variance_to_expected_variance_from_mean__{name_col_batch}{str_suffix_summarized_metrics}"
            name_col_score_for_selection = f"_float_score_highly_variable_feature__{name_col_batch}{str_suffix_summarized_metrics}"
            l_name_col_summarized = [
                name_col_sum,
                name_col_num_nonzero_values,
                name_col_mean,
                name_col_deviation,
                name_col_variance,
            ]  # define name_col, fill_value, dtype of the columns that will be summarized.
            l_fill_value = [0, 0, 0, np.nan, np.nan]
            l_dtype = [np.float64, np.float64, np.float64, np.float64, np.float64]
            flag_summarize_output_columns_already_exist = (
                len(
                    set(f"{name_layer}_{e}" for e in l_name_col_summarized).difference(
                        ax.meta.columns
                    )
                )
                == 0
            )  # retrieve a flag indicates the output columns of the summarize method are already exist in the metadata before initializing the columns
            for name_col, fill_value, dtype in zip(
                l_name_col_summarized
                + [
                    name_col_ratio_for_selection,
                    name_col_diff_for_selection,
                    name_col_score_for_selection,
                ],
                l_fill_value + [0, 0, 0],
                l_dtype + [np.float64, np.float64, np.float64],
            ):  # for each column, retrieve name_col, fill_value, and dtype
                name_col = f"{name_layer}_{name_col}"  # compose the name of the destination column
                ax.meta.initialize_column(
                    name_col,
                    dtype=dtype,
                    shape_not_primary_axis=(int_num_batches,),
                    chunks=(1,),
                    fill_value=fill_value,
                )  # chunk size is 1 to allow calculation of highly variabele genes for each batch separately.
                dict_metadata = ax.meta.get_column_metadata(
                    name_col
                )  # retrieve metadata
                dict_metadata[
                    "l_labels_1"
                ] = l_name_batch  # add cluster label information
                ax.meta.set_column_metadata(
                    name_col, dict_metadata
                )  # update column metadata

            def summarize_sum_and_dev_for_each_batch(
                self,
                int_entry_of_axis_for_querying,
                arr_int_entries_of_axis_not_for_querying,
                arr_value,
            ):
                """# 2023-04-28 04:35:02
                calculate sum and deviation of the values of the current entry

                assumes 'int_num_records' for each batch > 0
                """

                """ 
                collect values for each batch
                """
                dict_batch_to_arr_value = (
                    dict()
                )  # a dictionary that will contain arr_value for each batch
                for int_entries_of_axis_not_for_querying, value in zip(
                    arr_int_entries_of_axis_not_for_querying, arr_value
                ):
                    batch = dict_batch[int_entries_of_axis_not_for_querying]
                    if batch == -1:  # ignore NaN values, represented by the -1 value
                        continue
                    if batch not in dict_batch_to_arr_value:
                        dict_batch_to_arr_value[batch] = []
                    dict_batch_to_arr_value[batch].append(value)

                """ 
                summarize values for each batch
                """
                dict_summary = dict(
                    (name_col, np.full((int_num_batches,), fill_value, dtype=dtype))
                    for name_col, fill_value, dtype in zip(
                        l_name_col_summarized, l_fill_value, l_dtype
                    )
                )  # initialize 'dict_summary'
                for batch in list(
                    dict_batch_to_arr_value
                ):  # iterate over the list of available 'batch'
                    arr_value_of_a_batch = np.array(
                        dict_batch_to_arr_value.pop(batch), dtype=arr_value.dtype
                    )  # retrieve 'arr_value_of_a_batch' # convert to numpy array

                    int_num_records = len(
                        arr_value_of_a_batch
                    )  # retrieve the number of records of the current entry
                    int_total_num_entries_not_indexed = dict_batch_to_count[
                        batch
                    ]  # retrieve the total number of entries for a batch
                    dict_summary[name_col_sum][batch] = (
                        np.sum(arr_value_of_a_batch)
                        if int_num_records > 30
                        else sum(arr_value_of_a_batch)
                    )  # if an input array has more than 30 elements, use np.sum to calculate the sum
                    dict_summary[name_col_num_nonzero_values][batch] = int_num_records
                    dict_summary[name_col_mean][batch] = (
                        dict_summary[name_col_sum][batch]
                        / int_total_num_entries_not_indexed
                    )  # calculate the mean
                    arr_dev = (
                        arr_value_of_a_batch - dict_summary[name_col_mean][batch]
                    ) ** 2  # calculate the deviation
                    dict_summary[name_col_deviation][batch] = (
                        np.sum(arr_dev) if int_num_records > 30 else sum(arr_dev)
                    )
                    dict_summary[name_col_variance][batch] = (
                        dict_summary[name_col_deviation][batch]
                        / (int_total_num_entries_not_indexed - 1)
                        if int_total_num_entries_not_indexed > 1
                        else np.nan
                    )
                return dict_summary

            """
            (1) Calculate metrics for identification of highly variable features
            """
            # check if required metadata (mean and variance data of features) is not available, and if not, calculate and save the data
            if not flag_summarize_output_columns_already_exist:
                self.summarize(
                    name_layer=name_layer,
                    axis="feature",
                    summarizing_func=summarize_sum_and_dev_for_each_batch,
                    str_suffix=str_suffix_summarized_metrics,
                    l_name_col_summarized=l_name_col_summarized,
                )  # calculate mean and variance for features

            """
            (2) Identify highly variable genes for each sample
            """
            # add prefix to the output column names
            (
                name_col_sum_with_prefix,
                name_col_num_nonzero_values_with_prefix,
                name_col_mean_with_prefix,
                name_col_deviation_with_prefix,
                name_col_variance_with_prefix,
            ) = list(
                f"{name_layer}_{e}"
                for e in [
                    name_col_sum,
                    name_col_num_nonzero_values,
                    name_col_mean,
                    name_col_deviation,
                    name_col_variance,
                ]
            )  # add prefix
            (
                name_col_ratio_for_selection_with_prefix,
                name_col_diff_for_selection_with_prefix,
                name_col_score_for_selection_with_prefix,
            ) = list(
                f"{name_layer}_{e}"
                for e in [
                    name_col_ratio_for_selection,
                    name_col_diff_for_selection,
                    name_col_score_for_selection,
                ]
            )  # add prefix

            # initialize
            def __map__calculate_highly_variable_features(p_r, p_s):
                zdf_meta_fork_safe = zdf_meta.get_fork_safe_version(
                    flag_use_locking=False
                )  # get the fork-safe version, with loacking disabled (lock will be acquired in the main process, and since there will be no overlaps of chunks modified by individual worker processes, there is no need to acquire locks)
                while True:
                    """
                    Calculate metrics for identification of highly variable features
                    """
                    # receive the input
                    ins = p_r.recv()
                    if ins is None:
                        break
                    batch = ins  # parse input

                    # load mean and variance data in memory
                    arr_mean = zdf_meta_fork_safe[
                        name_col_mean_with_prefix, None, batch
                    ]
                    arr_var = zdf_meta_fork_safe[
                        name_col_variance_with_prefix, None, batch
                    ]

                    # learn mean-variance relationship for the data
                    mask = ~np.isnan(arr_var)  # exclude values containing np.nan
                    if (
                        mask.sum() == 0
                    ):  # contiue no valid data is available for fitting
                        p_s.send(np.nan)  # finish the task
                        continue
                    mean_var_relationship_fit = np.polynomial.polynomial.Polynomial.fit(
                        arr_mean[mask], arr_var[mask], 2
                    )  # fit using polynomial with degree 2
                    del mask  # delete temporary object

                    # initialize output values
                    n = len(arr_mean)  # the number of output entries
                    arr_ratio_of_variance_to_expected_variance_from_mean = np.full(
                        n, np.nan
                    )
                    arr_diff_of_variance_to_expected_variance_from_mean = np.full(
                        n, np.nan
                    )

                    for i in range(n):  # iterate each row
                        mean, var = arr_mean[i], arr_var[i]  # retrieve var and mean
                        if not np.isnan(var):  # if current entry is valid
                            var_expected = mean_var_relationship_fit(
                                mean
                            )  # calculate expected variance from the mean
                            if (
                                var_expected == 0
                            ):  # handle the case when the current expected variance is zero
                                arr_ratio_of_variance_to_expected_variance_from_mean[
                                    i
                                ] = np.nan
                                arr_diff_of_variance_to_expected_variance_from_mean[
                                    i
                                ] = np.nan
                            else:
                                arr_ratio_of_variance_to_expected_variance_from_mean[
                                    i
                                ] = (var / var_expected)
                                arr_diff_of_variance_to_expected_variance_from_mean[
                                    i
                                ] = (var - var_expected)

                    # add data to feature metadata
                    zdf_meta_fork_safe[
                        name_col_ratio_for_selection_with_prefix, None, batch
                    ] = arr_ratio_of_variance_to_expected_variance_from_mean
                    zdf_meta_fork_safe[
                        name_col_diff_for_selection_with_prefix, None, batch
                    ] = arr_diff_of_variance_to_expected_variance_from_mean

                    """
                    Calculate 'highly variable' score
                    """

                    def _calculate_weight(arr, thres: float, inplace: bool = True):
                        """# 2023-04-15 16:01:54
                        calculate weights using a threshold from a array of values (which will be modified in-place if 'inplace' is True).
                        the weight will be 1 if the value is same as or above the threshold. the weight will be 0 if the value is below 0. also, np.nan values will be replaced with 0
                        """
                        # handle invalid threshold
                        if thres <= 0:
                            return np.ones(
                                len(arr)
                            )  # use the same weight for all the entries
                        if not inplace:
                            arr = deepcopy(arr)
                        arr[arr > thres] = thres
                        arr /= thres  # normalize the weight
                        # replace invalid values
                        arr[arr < 0] = 0
                        arr[np.isnan(arr)] = 0
                        return arr

                    # calculate scores
                    arr_score = (
                        _calculate_weight(arr_mean, float_min_mean)
                        * _calculate_weight(arr_var, float_min_variance)
                        * arr_ratio_of_variance_to_expected_variance_from_mean
                        * arr_diff_of_variance_to_expected_variance_from_mean
                    )  # calculate the product of the ratio and difference of variance to expected variance for scoring and sorting highly variable features
                    zdf_meta_fork_safe[
                        name_col_score_for_selection_with_prefix, None, batch
                    ] = arr_score  # save the calculated scores

                    p_s.send(arr_score)  # return the result
                    del (
                        arr_ratio_of_variance_to_expected_variance_from_mean,
                        arr_diff_of_variance_to_expected_variance_from_mean,
                        arr_mean,
                        arr_var,
                    )
                zdf_meta_fork_safe.terminate_spawned_processes()  # terminate the servers

            arr_score_accumulated = np.zeros(
                len(zdf_meta), dtype=np.float64
            )  # intialize the accumulated scores

            def __reduce__calculate_highly_variable_features(res):
                if isinstance(
                    res, np.ndarray
                ):  # check whether the output is valid numpy array
                    res[np.isnan(res)] = 0  # replace np.nan values with 0 values
                    arr_score_accumulated[:] += res

            # lock the output columns
            ax.meta.lock(
                name_col_ratio_for_selection_with_prefix,
                name_col_diff_for_selection_with_prefix,
                name_col_score_for_selection_with_prefix,
            )

            bk.Multiprocessing_Batch_Generator_and_Workers(
                iter(l_batch_active),
                __map__calculate_highly_variable_features,
                __reduce__calculate_highly_variable_features,
                int_num_threads=self.int_num_cpus_for_updating_metadata,
            )

            # release the locks of the output columns
            ax.meta.unlock(
                name_col_ratio_for_selection_with_prefix,
                name_col_diff_for_selection_with_prefix,
                name_col_score_for_selection_with_prefix,
            )

            # save combined scores as a column
            int_num_batch_active = len(
                l_batch_active
            )  # retrieve the number of active batches
            ax.meta[
                f"{name_layer}__float_average_score_highly_variable_feature__{name_col_batch}{str_suffix_summarized_metrics}"
            ] = (
                arr_score_accumulated / int_num_batch_active
            )  # calculate the average scores of each feature and save the average scores as a column

            # save the filter
            if (
                int_num_highly_variable_features is None
            ):  # use all features with score > 0
                arr_filter = arr_score_accumulated > 0  # use all features with score
            else:  # if valid number of entries were given
                arr_filter = np.zeros(
                    ax.int_num_entries, dtype=bool
                )  # initialize the array
                arr_filter[
                    np.argsort(arr_score_accumulated)[
                        -int_num_highly_variable_features:
                    ]
                ] = True  # select the entries

            if name_col_filter is not None:  # if the name of the output column is valid
                ax.save_as_filter(
                    arr_filter, name_col_filter
                )  # save the filter using the given name

            if flag_load_filter:  # load the output filter
                ax.filter = arr_filter
        else:
            """
            # consider all the barcodes currently active in the RamData object as a single batch
            """
            """
            (1) Calculate metrics for identification of highly variable features
            """

            def __get_values(name_col, flag_all_rows: bool = False):
                """get values from the metadata ZDF
                flag_all_rows : bool = False # get values of all rows
                """
                if flag_all_rows:
                    return (
                        ax.meta[name_col, :, int_index_secondary]
                        if int_index_secondary is not None
                        else ax.meta[name_col, :]
                    )
                else:
                    return (
                        ax.meta[name_col, None, int_index_secondary]
                        if int_index_secondary is not None
                        else ax.meta[name_col]
                    )

            def __set_values(name_col, values, flag_all_rows: bool = False):
                """set values of the metadata ZDF
                flag_all_rows : bool = False # get values of all rows
                """
                if flag_all_rows:
                    if int_index_secondary is not None:
                        ax.meta[name_col, :, int_index_secondary] = values
                    else:
                        ax.meta[name_col, :] = values
                else:
                    if int_index_secondary is not None:
                        ax.meta[name_col, None, int_index_secondary] = values
                    else:
                        ax.meta[name_col] = values

            # set the name of the columns that will be used in the current method
            name_col_for_mean, name_col_for_variance = (
                f"{name_layer}_mean{str_suffix_summarized_metrics}",
                f"{name_layer}_variance{str_suffix_summarized_metrics}",
            )

            # check if required metadata (mean and variance data of features) is not available, and if not, calculate and save the metrics of the features
            if name_col_for_mean not in ax.meta or name_col_for_variance not in ax.meta:
                self.summarize(
                    name_layer,
                    "feature",
                    "sum_and_dev",
                    str_suffix=str_suffix_summarized_metrics,
                )  # calculate mean and variance for features

            # check if required metadata (mean and variance data of features) is not available, and if not, calculate and save the learned mean-variance relationship of the features.
            name_col_score = f"{name_layer}__float_score_highly_variable_feature{str_suffix_summarized_metrics}{str_suffix_mean_var_relationsip}"  # compose the name of the column that contains the scores for the selection of highly variable features
            if (
                name_col_score not in ax.meta
            ):  # if the output column does not exist, learn the mean-variance relationship
                # load mean and variance data in memory
                arr_mean = __get_values(name_col_for_mean)
                arr_var = __get_values(name_col_for_variance)

                if flag_show_graph:
                    plt.plot(arr_mean[::10], arr_var[::10], ".", alpha=0.01)
                    bk.MATPLOTLIB_basic_configuration(
                        x_scale="log",
                        y_scale="log",
                        x_label="mean",
                        y_label="variance",
                        title=f"mean-variance relationship\nin '{name_layer}'",
                    )
                    plt.show()

                # learn mean-variance relationship for the data
                mask = ~np.isnan(arr_var)  # exclude values containing np.nan
                if mask.sum() == 0:  # exit if no valid data is available for fitting
                    return
                mean_var_relationship_fit = np.polynomial.polynomial.Polynomial.fit(
                    arr_mean[mask], arr_var[mask], 2
                )  # fit using polynomial with degree 2
                del mask  # delete temporary object

                # initialize output values
                n = len(arr_mean)  # the number of output entries
                arr_ratio_of_variance_to_expected_variance_from_mean = np.full(
                    n, np.nan
                )
                arr_diff_of_variance_to_expected_variance_from_mean = np.full(n, np.nan)

                for i in range(n):  # iterate each row
                    mean, var = arr_mean[i], arr_var[i]  # retrieve var and mean
                    if not np.isnan(var):  # if current entry is valid
                        var_expected = mean_var_relationship_fit(
                            mean
                        )  # calculate expected variance from the mean
                        if (
                            var_expected == 0
                        ):  # handle the case when the current expected variance is zero
                            arr_ratio_of_variance_to_expected_variance_from_mean[
                                i
                            ] = np.nan
                            arr_diff_of_variance_to_expected_variance_from_mean[
                                i
                            ] = np.nan
                        else:
                            arr_ratio_of_variance_to_expected_variance_from_mean[i] = (
                                var / var_expected
                            )
                            arr_diff_of_variance_to_expected_variance_from_mean[i] = (
                                var - var_expected
                            )

                # add data to the feature metadata
                __set_values(
                    f"{name_layer}__float_ratio_of_variance_to_expected_variance_from_mean{str_suffix_summarized_metrics}{str_suffix_mean_var_relationsip}",
                    arr_ratio_of_variance_to_expected_variance_from_mean,
                )
                __set_values(
                    f"{name_layer}__float_diff_of_variance_to_expected_variance_from_mean{str_suffix_summarized_metrics}{str_suffix_mean_var_relationsip}",
                    arr_diff_of_variance_to_expected_variance_from_mean,
                )
                __set_values(
                    name_col_score,
                    arr_ratio_of_variance_to_expected_variance_from_mean
                    * arr_diff_of_variance_to_expected_variance_from_mean,
                )  # calculate the product of the ratio and difference of variance to expected variance for scoring and sorting highly variable features # save the scores

            """
            (2) identify of highly variable features
            """
            # reset the feature filter prior to retrieve the metadata of all features
            ba = ax.all() if ax.filter is None else ax.filter  # retrieve filter

            # filter using variance and mean values
            ba = ax.AND(
                ba,
                __get_values(name_col_for_variance, flag_all_rows=True)
                > float_min_variance,
                __get_values(name_col_for_mean, flag_all_rows=True) > float_min_mean,
            )
            ax.filter = ba

            if len(ax.meta) < int_num_highly_variable_features:
                if self.verbose:
                    logger.info(
                        f"[RamData.identify_highly_variable_features] there are only {len( ax.meta )} number of features satisfying the thresholds, 'int_num_highly_variable_features' will be modified."
                    )
                int_num_highly_variable_features = len(ax.meta)

            # calculate a threshold for highly variable score
            arr_scores = __get_values(name_col_score)  # retrieve the scores
            float_min_score_highly_variable = arr_scores[
                np.lexsort((__get_values(name_col_for_mean), arr_scores))[
                    -int_num_highly_variable_features
                ]
            ]
            del arr_scores

            # filter using highly variable score
            ax.filter = None
            ba = ax.AND(
                ba,
                __get_values(name_col_score, flag_all_rows=True)
                > float_min_score_highly_variable,
            )

            if name_col_filter is not None:  # if the name of the output column is valid
                ax.save_as_filter(
                    ba, name_col_filter
                )  # save the filter using the given name

            if (
                not flag_load_filter
            ):  # if filter should not be loaded, restore the filter
                ax.filter = ba_filter_backup  # restore the previously set filter once all operations were completed
            else:
                ax.filter = ba  # load the output filter

    """ function for fast exploratory analysis """

    def prepare_dimension_reduction_from_raw(
        self,
        name_layer_raw: Union[str, None] = "raw",
        name_layer_raw_copy: Union[str, None] = "raw_copy",
        name_layer_normalized: Union[str, None] = "normalized",
        name_layer_log_transformed: Union[str, None] = "normalized_log1p",
        name_layer_scaled: str = "normalized_log1p_scaled",
        name_layer_capped: str = "normalized_log1p_capped",
        name_col_filter_filtered_barcode: str = "filtered_barcodes",
        min_counts: int = 500,
        min_features: int = 100,
        int_total_count_target: int = 10000,
        int_num_highly_variable_features: int = 2000,
        max_value: float = 10,
        name_col_filter_highly_variable="filter_normalized_log1p_highly_variable",
        dict_kw_hv: dict = {
            "float_min_mean": 0.01,
            "float_min_variance": 0.01,
            "str_suffix_summarized_metrics": "",
        },
        flag_use_fast_mode: bool = True,
        flag_copy_raw_from_remote_source: bool = True,
        flag_skip_total_count_calculation: bool = False,
        flag_skip_variance_calculation: bool = False,
        name_col_total_count: Union[str, None] = None,
        name_col_variance: Union[str, None] = None,
        int_index_component_reference: Union[int, None] = None,
    ):
        """# 2023-03-11 22:51:24
        This function provides convenience interface for pre-processing step for preparing normalized, scaled expression data for PCA dimension reduction
        assumes raw count data (or the equivalent of it) is available in 'dense' format (local) or 'sparse_for_querying_features' and 'sparse_for_querying_barcodes' format (remote source)

        # Fast mode
        - rely on a single dense RAMtx containing raw count data
        - only a single output layer with sparse RAMtx (that can be queried for each barcode) will be generated, containing filtered barcoes and only highly variable genes.

        # Slow mode
        - sparse RAMtx will be generated for every layer
        - all features, all barcodes will be available in the layer, which reduce time for re-analysis


        === general ===
        flag_use_fast_mode : bool = True : if True, a fast method designed for fast global exploratory analysis (UMAP projection) of the raw data, removing unncessary layer building operations as much as possible. if False, every layer will be written to disk, unfiltered (containing all barcodes and features). 'slow' mode will be much slower but can be re-analyzed more efficiently later (subclustering, etc.)
        flag_copy_raw_from_remote_source : bool = True # create a copy of the raw layer locally for faster access (caching) if the raw layer exists in the remote source.

        === input/output layers ===
        name_layer_raw : str = 'raw' # the name of the layer containing 'raw' count data
        name_layer_raw_copy : str = 'raw_copy' # the name of the layer containing copied 'raw' count data, copied from the remote source
        name_layer_normalized : str = 'normalized' # the name of the layer containing normalized raw count data
        name_layer_log_transformed : str = 'normalized_log1p' # the name of the layer containing log-transformed normalized raw count data
        name_layer_capped : str = 'normalized_log1p_capped', # the name of the layer containing capped, log-transformed normalized raw count data
        name_layer_scaled : str = 'normalized_log1p_scaled' # the name of the layer that will contain the log-normalized, scale gene expression data in a 'sparse_for_querying_barcodes' ramtx mode of only the highly variable genes, selected by the current filter settings, 'int_num_highly_variable_features', and 'dict_kw_hv' arguments. data will be scaled and capped according to 'max_value' arguments

        === barcode filtering ===
        name_col_filter_filtered_barcode : str = 'filtered_barcodes' # the name of metadata column that will contain filter containing active barcode entries after barcode filtering

        'int_total_count_target' : total count target for normalization
        'min_counts' = 500, 'min_features' = 100 : for barcode filtering

        === highly variable feature detection ===
        'int_num_highly_variable_features' : the number of highly variable genes to retrieve
        'dict_kw_hv' : settings for 'RamData.identify_highly_variable_features'

        === normalization ===
        int_total_count_target : int = 10000 # total target count of cells
        name_col_total_count : Union[ str, None ] = None # name of column of the 'barcodes' metadata containing the total count of barcodes

        === capping & scaling ===
        max_value : float = 10,  : capping at this value during scaling/capping
        name_col_variance : Union[ str, None ] = None # name of column of the 'features' metadata containing variance of the features

        === reference-based scaling ===
        int_index_component_reference : Union[ int, None ] = None # The index of the RamData component (if current RamData contains multiple component RamData using 'combined' mode).
            By default data from all components will be processed together.
            If an index to the RamData component was given,
                (1) whether the component has the given column containing variance of normalized, log-transformed values, and
                (2) whether the component has the given column containing filter for highly variable genes that was used to build PCA values
                will be checked.

        flag_skip_total_count_calculation : bool = False # if True, skip calculation of total counts for each barcode
        flag_skip_variance_calculation : bool = False # if True, skip calculation of variance of each feature
        """
        # set default 'index_component_reference'
        if self.is_combined:
            if int_index_component_reference is None:
                int_index_component_reference = self.int_index_component_reference
        else:
            int_index_component_reference = None

        # set the reference
        if (
            self.is_combined and int_index_component_reference is not None
        ):  # if current RamData is 'combined' mode and 'int_index_component_reference' has been set
            # default 'int_index_component_reference' when 'int_index_component_reference' is invalid is 0
            if not (0 <= int_index_component_reference < self.int_num_components):
                int_index_component_reference = 0

            # set barcode filters excluding barcodes from the reference
            ba_filter_all_components = (
                self.bc.filter
            )  # backup the filter before modifying the filter
            self.bc.filter = (
                self.bc.all() if self.bc.filter is None else self.bc.filter
            ) & (
                ~self.bc.select_component(int_index_component_reference)
            )  # exclude entries of the reference component

        # set default column names
        name_col_total_count = (
            f"{name_layer_raw}_sum"
            if name_col_total_count is None
            else name_col_total_count
        )
        name_col_variance = (
            f"{name_layer_log_transformed}_variance"
            if name_col_variance is None
            else name_col_variance
        )

        # load a raw count layer
        if name_layer_raw is not None:  # check validity of name_layer
            self.layer = name_layer_raw  # load the 'raw' layer
            # if the input matrix is 'dense', prepare operation for dense matrix
            if "dense" in self.layer:
                self.layer[
                    "dense"
                ].survey_number_of_records_for_each_entry()  # prepare operation on dense RAMtx

        # in 'slow' mode, use sparse matrix for more efficient operation
        if (
            not flag_use_fast_mode and name_layer_raw is not None
        ):  # check validity of name_layer
            # if 'dense' matrix is available, convert dense to sparse formats
            if "dense" in self.layer:
                """%% SLOW MODE %%"""
                if self.verbose:
                    logger.info(
                        f"[RamData.prepare_dimension_reduction_from_raw] [SLOW MODE] converting dense to sparse formats ... "
                    )
                # dense -> sparse conversion
                self.apply(
                    name_layer_raw,
                    name_layer_raw,
                    "ident",
                    mode_instructions=[
                        ["dense", "sparse_for_querying_features"],
                        ["dense", "sparse_for_querying_barcodes"],
                    ],
                )  # assumes raw count data (or the equivalent of it) is available in 'dense' format (local)

        # copy raw count data available remotely to local storage for caching
        flag_raw_in_remote_location = (
            self.contains_remote
            and name_layer_raw in self.layers
            and name_layer_raw not in self.layers_excluding_components
        )  # retrieve a flag indicating raw count data resides in remote location
        if (
            flag_raw_in_remote_location
            and flag_copy_raw_from_remote_source
            and name_layer_raw_copy is not None
        ):  # check validity of name_layer
            if self.verbose:
                logger.info(
                    f"[RamData.prepare_dimension_reduction_from_raw] copying raw count data available in remote source to local storage ... "
                )
            self.apply(
                name_layer_raw,
                name_layer_raw_copy,
                "ident",
                mode_instructions=[
                    ["sparse_for_querying_features", "sparse_for_querying_features"],
                    ["sparse_for_querying_barcodes", "sparse_for_querying_barcodes"],
                ],
            )  # copy raw count data to local storage # assumes raw count data (or the equivalent of it) is available in 'sparse_for_querying_features' and 'sparse_for_querying_barcodes' format (remote source)
            name_layer_raw = (
                name_layer_raw_copy  # use 'name_layer_raw_copy' as 'name_layer_raw'
            )
            self.layer = name_layer_raw_copy  # load the layer

        # calculate total counts for each barcode
        if (
            name_layer_raw is not None and not flag_skip_total_count_calculation
        ):  # check validity of name_layer
            if self.verbose:
                logger.info(
                    f"[RamData.prepare_dimension_reduction_from_raw] summarizing total count for each barcode ... "
                )

            # fall back for invalid 'name_col_total_count'
            if name_col_total_count != f"{name_layer_raw}_sum":
                if self.verbose:
                    logger.info(
                        f"[RamData.prepare_dimension_reduction_from_raw] given column name for total count, '{name_col_total_count}' does not exist in the barcode metadata, falling back to '{name_layer_raw}_sum' column"
                    )
                name_col_total_count = f"{name_layer_raw}_sum"

            # calculate total counts for each barcode
            if (
                name_col_total_count not in self.bc.meta
            ):  # if an output column does not exists
                self.summarize(name_layer_raw, "barcode", "sum")

        # filter cells
        ba_filter_bc_back_up = (
            self.bc.filter
        )  # back up the filter of the 'barcodes' axis
        if (
            name_col_filter_filtered_barcode is not None
        ):  # check validity of 'name_col_filter_filtered_barcode' column
            if self.verbose:
                logger.info(
                    f"[RamData.prepare_dimension_reduction_from_raw] filtering barcodes ... "
                )
            if (
                name_col_filter_filtered_barcode in self.bc.meta
            ):  # if the filter is available, load the filter
                self.bc.change_filter(name_col_filter_filtered_barcode)
            else:  # if the filter is not available, filter barcodes based on the settings
                self.bc.filter = (
                    (
                        self.bc.all(
                            flag_return_valid_entries_in_the_currently_active_layer=False
                        )
                        if self.bc.filter is None
                        else self.bc.filter
                    )
                    & BA.to_bitarray(
                        self.bc.meta[f"{name_layer_raw}_sum", :] > min_counts
                    )
                    & BA.to_bitarray(
                        self.bc.meta[f"{name_layer_raw}_num_nonzero_values", :]
                        > min_features
                    )
                )  # set 'flag_return_valid_entries_in_the_currently_active_layer' to False in order to avoid surveying the combined RamData layer
                self.bc.save_filter(
                    name_col_filter_filtered_barcode
                )  # save filter for later analysis
            if self.verbose:
                logger.info(
                    f"[RamData.prepare_dimension_reduction_from_raw] filtering completed."
                )

        if flag_use_fast_mode:
            """%% FAST MODE %%"""
            """
            %% HVG detection %%
            """
            # retrieve total raw count data for normalization
            self.bc.meta.load_as_dict(name_col_total_count)
            dict_count = self.bc.meta.dict.pop(
                name_col_total_count
            )  # retrieve total counts for each barcode as a dictionary

            # retrieve the total number of barcodes
            int_total_num_barcodes = self.bc.meta.n_rows

            # define name of the output keys
            name_key_sum = f"{name_layer_log_transformed}_sum"
            name_key_mean = f"{name_layer_log_transformed}_mean"
            name_key_deviation = f"{name_layer_log_transformed}_deviation"
            name_key_variance = f"{name_layer_log_transformed}_variance"

            def func(
                self,
                int_entry_of_axis_for_querying: int,
                arr_int_entries_of_axis_not_for_querying: np.ndarray,
                arr_value: np.ndarray,
            ):  # normalize count data of a single feature containing (possibly) multiple barcodes
                """# 2022-07-06 23:58:38"""
                # perform normalization in-place
                for i, e in enumerate(
                    arr_int_entries_of_axis_not_for_querying.astype(int)
                ):  # iterate through barcodes
                    arr_value[i] = (
                        arr_value[i] / dict_count[e]
                    )  # perform normalization using the total count data for each barcode
                arr_value *= int_total_count_target

                # perform log1p transformation
                arr_value = np.log10(arr_value + 1)

                # calculate deviation
                int_num_records = len(
                    arr_value
                )  # retrieve the number of records of the current entry
                dict_summary = {
                    name_key_sum: np.sum(arr_value)
                    if int_num_records > 30
                    else sum(arr_value)
                }  # if an input array has more than 30 elements, use np.sum to calculate the sum
                dict_summary[name_key_mean] = (
                    dict_summary[name_key_sum] / int_total_num_barcodes
                )  # calculate the mean
                arr_dev = (
                    arr_value - dict_summary[name_key_mean]
                ) ** 2  # calculate the deviation
                dict_summary[name_key_deviation] = (
                    np.sum(arr_dev) if int_num_records > 30 else sum(arr_dev)
                )
                dict_summary[name_key_variance] = (
                    dict_summary[name_key_deviation] / (int_total_num_barcodes - 1)
                    if int_total_num_barcodes > 1
                    else np.nan
                )
                return dict_summary

            # calculate the metric for identifying highly variable genes
            if not flag_skip_variance_calculation:
                if self.verbose:
                    logger.info(
                        f"[RamData.prepare_dimension_reduction_from_raw] [FAST MODE] calculating metrics for highly variable feature detection ... "
                    )
                self.summarize(
                    name_layer_raw,
                    "feature",
                    func,
                    l_name_col_summarized=[
                        name_key_sum,
                        name_key_mean,
                        name_key_deviation,
                        name_key_variance,
                    ],
                    str_prefix="",
                )  # set prefix as ''

            # identify highly variable genes
            self.identify_highly_variable_features(
                name_layer=name_layer_log_transformed,
                int_num_highly_variable_features=int_num_highly_variable_features,
                flag_show_graph=True,
                flag_load_filter=True,
                name_col_filter=name_col_filter_highly_variable,
                **dict_kw_hv,
            )

            if name_layer_capped is not None and max_value is not None:
                """
                %% capping %%
                """

                # write log-normalized and capped data for the selected highly variable features
                def func(
                    self,
                    int_entry_of_axis_for_querying,
                    arr_int_entries_of_axis_not_for_querying,
                    arr_value,
                ):
                    """# 2022-07-06 23:58:38"""
                    # perform normalization
                    arr_value *= (
                        int_total_count_target
                        / dict_count[int_entry_of_axis_for_querying]
                    )  # perform normalization using the total count data for each barcode

                    # perform log1p transformation
                    arr_value = np.log10(arr_value + 1)

                    # capping values above 'max_value'
                    arr_value[arr_value > max_value] = max_value

                    # return results
                    return (
                        int_entry_of_axis_for_querying,
                        arr_int_entries_of_axis_not_for_querying,
                        arr_value,
                    )

                if self.verbose:
                    logger.info(
                        f"[FAST MODE] write log-normalized and capped data for the selected highly variable features ... "
                    )
                self.apply(
                    name_layer_raw,
                    name_layer_capped,
                    func,
                    [["sparse_for_querying_barcodes", "sparse_for_querying_barcodes"]],
                )  # use sparse input as a source if available

            if name_layer_scaled is not None and name_col_variance is not None:
                """
                %% scaling %%
                """
                # retrieve flags
                flag_cap_value = max_value is not None
                flag_divide_by_sd = (
                    name_col_variance is not None
                    and name_col_variance in self.ft.columns
                )  # the 'name_col_variance' column name should be present in the metadata zdf.

                # retrieve variance
                self.ft.meta.load_as_dict(name_col_variance)
                dict_var = self.ft.meta.dict.pop(
                    name_col_variance
                )  # retrieve total counts for each barcode as a dictionary

                # write log-normalized, scaled, and capped data for the selected highly variable features
                def func(
                    self,
                    int_entry_of_axis_for_querying,
                    arr_int_entries_of_axis_not_for_querying,
                    arr_value,
                ):
                    """# 2022-07-06 23:58:38"""
                    # perform normalization
                    arr_value *= (
                        int_total_count_target
                        / dict_count[int_entry_of_axis_for_querying]
                    )  # perform normalization using the total count data for each barcode

                    # perform log1p transformation
                    arr_value = np.log10(arr_value + 1)

                    # perform scaling in-place
                    for i, e in enumerate(
                        arr_int_entries_of_axis_not_for_querying.astype(int)
                    ):  # iterate through features
                        float_var = dict_var[e]  # retrieve variance
                        if (
                            float_var != 0
                        ):  # if standard deviation is not available, use the data as-is
                            arr_value[i] = (
                                arr_value[i] / float_var**0.5
                            )  # retrieve standard deviation of the current feature from the variance # perform scaling of data for each feature

                    if flag_cap_value:
                        arr_value[
                            arr_value > max_value
                        ] = max_value  # capping values above 'max_value'

                    # return results
                    return (
                        int_entry_of_axis_for_querying,
                        arr_int_entries_of_axis_not_for_querying,
                        arr_value,
                    )

                if self.verbose:
                    logger.info(
                        f"[FAST MODE] write log-normalized, scaled, and capped data for the selected highly variable features ... "
                    )
                self.apply(
                    name_layer_raw,
                    name_layer_scaled,
                    func,
                    [["sparse_for_querying_barcodes", "sparse_for_querying_barcodes"]],
                )  # use sparse input as a source if available
        else:
            """%% SLOW MODE %%"""
            self.bc.filter = ba_filter_bc_back_up  # restore the barcode filter (in order to contain records of all barcodes in the output layers)

            # normalize
            if name_layer_normalized is not None and name_layer_raw is not None:
                self.normalize(
                    name_layer_raw,
                    name_layer_normalized,
                    name_col_total_count=name_col_total_count,
                    int_total_count_target=int_total_count_target,
                    mode_instructions=[
                        [
                            "sparse_for_querying_features",
                            "sparse_for_querying_features",
                        ],
                        [
                            "sparse_for_querying_barcodes",
                            "sparse_for_querying_barcodes",
                        ],
                    ],
                )

            # log-transform
            if (
                name_layer_log_transformed is not None
                and name_layer_normalized is not None
            ):
                self.apply(
                    name_layer_normalized,
                    name_layer_log_transformed,
                    "log1p",
                    mode_instructions=[
                        [
                            "sparse_for_querying_features",
                            "sparse_for_querying_features",
                        ],
                        [
                            "sparse_for_querying_barcodes",
                            "sparse_for_querying_barcodes",
                        ],
                    ],
                )

            # cap
            if name_layer_log_transformed is not None and name_layer_capped is not None:
                self.apply(
                    name_layer_log_transformed,
                    name_layer_capped,
                    "ident",
                    mode_instructions=[
                        [
                            "sparse_for_querying_features",
                            "sparse_for_querying_features",
                        ],
                        [
                            "sparse_for_querying_barcodes",
                            "sparse_for_querying_barcodes",
                        ],
                    ],
                )

            # load filter for filtered barcodes (if the filter exists)
            if (
                name_col_filter_filtered_barcode in self.bc.meta
            ):  # check validity of the name_col
                self.bc.change_filter(name_col_filter_filtered_barcode)

            # identify highly variable features (with filtered barcodes)
            self.identify_highly_variable_features(
                name_layer_log_transformed,
                int_num_highly_variable_features=int_num_highly_variable_features,
                flag_show_graph=True,
                flag_load_filter=False,  # clear feature filter (in order to contain records of every features in the output layer)
                name_col_filter=name_col_filter_highly_variable,
                **dict_kw_hv,
            )

            # scale data (with metrics from the filtered barcodes)
            if (
                name_layer_scaled is not None and name_layer_log_transformed is not None
            ):  # check validity of name_layer
                self.scale(
                    name_layer_log_transformed,
                    name_layer_scaled,
                    name_col_variance=name_col_variance,
                    max_value=max_value,
                    mode_instructions=[
                        [
                            "sparse_for_querying_features",
                            "sparse_for_querying_features",
                        ],
                        [
                            "sparse_for_querying_barcodes",
                            "sparse_for_querying_barcodes",
                        ],
                    ],
                )  # scale data

        # restore filter containing all components
        if int_index_component_reference is not None:
            self.bc.filter = ba_filter_all_components

    def perform_dimension_reduction_and_clustering(
        self,
        name_layer_pca: str,
        name_filter_barcodes: str,
        name_filter_features: Union[str, None] = None,
        int_num_components: int = 30,
        int_num_barcodes_in_pumap_batch: int = 50000,
        int_num_barcodes_for_a_batch: int = 50000,
        float_prop_subsampling_pca: float = 0.5,
        str_suffix: str = "",
        flag_subsample: bool = True,
        dict_kw_subsample: dict = dict(),
        flag_skip_pca: bool = False,
        str_embedding_method: Literal[
            "pumap", "scanpy-umap", "scanpy-tsne", "knn_embedder", "knngraph"
        ] = "pumap",
        dict_kw_for_run_scanpy_using_pca={
            "int_neighbors_n_neighbors": 10,
            "int_neighbors_n_pcs": 30,
            "set_method": {"leiden", "umap"},
            "dict_kw_umap": dict(),
            "dict_kw_leiden": {"resolution": 1},
            "dict_kw_tsne": dict(),
        },
    ):
        """# 2022-11-16 17:53:57
        perform dimension rediction and clustering

        'name_layer_pca' : the name of the layer to retrieve expression data for building PCA values
        'name_filter_barcodes' : the name of the filter containing the barcode entries that will be analyzed by the current function
        'name_filter_features' : the name of the filter containing the features entries from which PCA values will be calculated. By default, all currently active features will be used
        'int_num_components' : the number of PCA components to use
        'flag_subsample' : if True, perform subsampling. if False, perform leiden clustering and UMAP embedding using all barcodes.
        'str_suffix' : a suffix to add to the name of the results.

        'flag_skip_pca' : bool = False # skip PCA calculation step
        """
        # load features filter if available
        if name_filter_features is not None:
            self.ft.change_filter(name_filter_features)

        # calculate PCA values
        if not flag_skip_pca:  # calculate PCA values
            self.train_pca(
                name_layer=name_layer_pca,
                int_num_components=int_num_components,
                int_num_barcodes_in_ipca_batch=int_num_barcodes_for_a_batch,
                name_col_filter=f"filter_pca{str_suffix}",
                float_prop_subsampling=float_prop_subsampling_pca,
                name_col_filter_subsampled=f"filter_pca_subsampled{str_suffix}",
                flag_ipca_whiten=False,
                name_model=f"ipca{str_suffix}",
                int_num_threads=3,
                flag_show_graph=True,
            )

            self.apply_pca(
                name_model=f"ipca{str_suffix}",
                name_layer=name_layer_pca,
                name_col=f"X_pca{str_suffix}",
                name_col_filter=name_filter_barcodes,
                int_n_components_in_a_chunk=20,
                int_num_threads=5,
            )

        """ # 2022-11-16 17:43:05 
        Under constructions
        """
        if "scanpy-" in str_embedding_method:
            self.run_scanpy_using_pca(
                name_col_pca=f"X_pca{str_suffix}",
                int_num_pca_components=int_num_components,
                str_suffix=str_suffix,
                **dict_kw_for_run_scanpy_using_pca,
            )
        else:
            # legacy embedding methods using pumap
            if flag_subsample:  # perform subsampling for clustering and embedding
                self.subsample(
                    int_num_entries_to_use=int_num_barcodes_for_a_batch,
                    int_num_entries_to_subsample=int_num_barcodes_in_pumap_batch,
                    name_col_data=f"X_pca{str_suffix}",
                    name_col_label=f"subsampling_label{str_suffix}",
                    name_col_avg_dist=f"subsampling_avg_dist{str_suffix}",
                    axis="barcodes",
                    name_col_filter=name_filter_barcodes,
                    name_col_filter_subsampled=f"filter_subsampled{str_suffix}",
                    int_num_entries_in_a_batch=int_num_barcodes_for_a_batch,
                    **dict_kw_subsample,
                )

                self.bc.change_filter(f"filter_subsampled{str_suffix}")
                self.train_umap(
                    name_col_pca=f"X_pca{str_suffix}",
                    int_num_components_pca=int_num_components,
                    int_num_components_umap=2,
                    name_col_filter=f"filter_subsampled{str_suffix}",
                    name_pumap_model=f"pumap{str_suffix}",
                )

                # 2nd training
                self.bc.change_filter(name_filter_barcodes)
                self.bc.filter = self.bc.subsample(
                    min(1, int_num_barcodes_in_pumap_batch / self.bc.filter.count())
                )
                self.bc.save_filter(f"filter_subsampled_randomly{str_suffix}")
                self.train_umap(
                    name_col_pca=f"X_pca{str_suffix}",
                    int_num_components_pca=int_num_components,
                    int_num_components_umap=2,
                    name_col_filter=f"filter_subsampled_randomly{str_suffix}",
                    name_pumap_model=f"pumap{str_suffix}",
                )
            else:  # use all barcodes for clustering
                self.leiden(
                    f"leiden{str_suffix}",
                    name_col_data=f"X_pca{str_suffix}",
                    int_num_components_data=int_num_components,
                    name_col_label=f"leiden{str_suffix}",
                    resolution=0.2,
                    name_col_filter=name_filter_barcodes,
                )

                self.bc.change_filter(name_filter_barcodes)
                self.train_umap(
                    name_col_pca=f"X_pca{str_suffix}",
                    int_num_components_pca=int_num_components,
                    int_num_components_umap=2,
                    name_col_filter=name_filter_barcodes,
                    name_pumap_model=f"pumap{str_suffix}",
                )

            # apply umap
            self.apply_umap(
                name_col_pca=f"X_pca{str_suffix}",
                name_col_umap=f"X_umap{str_suffix}",
                int_num_barcodes_in_pumap_batch=int_num_barcodes_for_a_batch,
                name_col_filter=name_filter_barcodes,
                name_pumap_model=f"pumap{str_suffix}",
            )

    """ utility functions for filter """

    def change_filter(
        self, name_col_filter=None, name_col_filter_bc=None, name_col_filter_ft=None
    ) -> None:
        """# 2022-07-16 17:27:58
        retrieve and apply filters for 'barcode' and 'feature' Axes

        'name_col_filter_bc', 'name_col_filter_ft' will override 'name_col_filter' when applying filters.
        if all name_cols are invalid, no filters will be retrieved and applied
        """
        # check validity of name_cols for filter
        # bc
        if name_col_filter_bc not in self.bc.meta:
            name_col_filter_bc = (
                name_col_filter if name_col_filter in self.bc.meta else None
            )  # use 'name_col_filter' instead if 'name_col_filter_bc' is invalid
        # ft
        if name_col_filter_ft not in self.ft.meta:
            name_col_filter_ft = (
                name_col_filter if name_col_filter in self.ft.meta else None
            )  # use 'name_col_filter' instead if 'name_col_filter_ft' is invalid

        # apply filters
        self.bc.change_filter(name_col_filter_bc)  # bc
        self.ft.change_filter(name_col_filter_ft)  # ft

    def save_filter(
        self, name_col_filter=None, name_col_filter_bc=None, name_col_filter_ft=None
    ) -> None:
        """# 2022-07-16 17:27:54
        save filters for 'barcode' and 'feature' Axes

        'name_col_filter_bc', 'name_col_filter_ft' will override 'name_col_filter' when saving filters
        for consistency, if filter has not been set, filter containing all active entries (containing valid count data) will be saved instead

        if all name_cols are invalid, no filters will be saved
        """
        # save filters
        self.bc.save_filter(
            name_col_filter if name_col_filter_bc is None else name_col_filter_bc
        )  # bc
        self.ft.save_filter(
            name_col_filter if name_col_filter_ft is None else name_col_filter_ft
        )  # ft

    def change_or_save_filter(
        self, name_col_filter=None, name_col_filter_bc=None, name_col_filter_ft=None
    ) -> None:
        """# 2022-08-07 02:03:53
        retrieve and apply filters for 'barcode' and 'feature' Axes, and if the filter names do not exist in the metadata and thus cannot be retrieved, save the currently active entries of each axis to its metadata using the given filter name.

        'name_col_filter_bc', 'name_col_filter_ft' will override 'name_col_filter' when saving filters
        for consistency, if filter has not been set, filter containing all active entries (containing valid count data) will be saved instead

        if all name_cols are invalid, no filters will be saved/retrieved
        """
        # load or save filters ('name_col_filter_bc', 'name_col_filter_ft' get priority over 'name_col_filter')
        self.bc.change_or_save_filter(
            name_col_filter if name_col_filter_bc is None else name_col_filter_bc
        )  # bc
        self.ft.change_or_save_filter(
            name_col_filter if name_col_filter_ft is None else name_col_filter_ft
        )  # ft
        return

    """ utility functions for retrieving expression values from layer and save them as metadata in axis  """

    def get_expr(
        self,
        queries,
        float_min_expr: Union[float, None] = None,
        name_col_label: Union[str, None] = None,
        float_min_prop_in_a_label: float = 0.1,
        flag_AND_operation: bool = False,
        name_new_col: Union[str, None] = None,
        name_layer: Union[str, None] = None,
        axis: Union[int, str] = "features",
    ):
        """# 2023-01-17 15:10:42
        retrieve expression values of given 'queries' from the given layer 'name_layer' in the given axis 'axis' (with currently active filters),
        and save the total expression values for each entry in the axis metadata using the new column name 'name_new_col'

        possible usages: (1) calculating gene_set/pathway activities across cells, which can subsequently used for filtering cells for subclustering
                         (2) calculating pseudo-bulk expression profiles of a subset of cells across all active features
                         (3) retrieving a filter for barcodes expressing certein set of features of the threshold for subclustering (expression-based cell selection)
                         (4) retrieving a filter for barcodes of cluster labels expressing certein proportion of set of features of the threshold for subclustering (expression- and cluster-based cell selection)

        'name_layer' : name of the layer to retrieve data
        'queries' : queries that will be handed to RamDataAxis.__getitem__ calls. A slice, a bitarray, a single or a list of integer representation(s), a single or a list of string representation(s), boolean array are one of the possible inputs
        'name_new_col' : the name of the new column that will contains retrieved expression values in the metadata of the given axis. if None, does not
        'axis' : axis for querying. { 1 or 'features' } for summarizing expression on the 'barcodes' axis, and { 0 or 'barcodes' } for summarizing expression on the 'features' axis.

        ===== arguments for creating a filter (selecting barcodes) for subclustering ====
        By default, 'get_expr' method return a 1D array with the length of the unfiltered axis. However, the conversion of sparse matrix into dense matrix and sum operation takes a lot of computational time (for 50M length axis, retrieving data from RAMtx takes 0.5s but retrieving 1D array took 12 seconds, using a single core).
        Therefore, for the purpose of filtering barcodes/features, it is better to directly process the sparse matrix without conversion to dense matrix.
        To enable this feature, set 'float_min_expr' to non-None value

        float_min_expr : Union[ float, None ] = None, # mark barcodes/features above this threshold to 1
        name_col_label : Union[ str, None ] = None, # the name of the column to retrieve the cluster information of the entries in the axis.
        float_min_prop_in_a_label : Union[ float, None ] = 0.1, # a minimum proportion of entries that are marked as 1 in a cluster label (only considering the entries that are currently active in the filter) to include all the entries of the cluster. if the proportion does not reach this minimum value, all entries in the cluster will not be included in the mask
        flag_AND_operation : bool = False, # if True, the mask from each queried feature/barcode will be combined into a single mask using AND operation. if False, the mask from each queried feature/barcode will be combined using OR operation.
        """
        # handle attributes
        flag_retrieve_mask = (
            float_min_expr is not None
        )  # retrieve a flag indicating a mask is retrieved
        flag_using_cluster_label_for_retrieving_mask = (
            name_col_label is not None
        )  # retrieve a flag indicating the cluster information is used

        # handle inputs
        flag_axis_for_querying_is_barcode = self._determine_axis(
            axis
        )  # retrieve a flag indicating whether the barcode are being queried.

        # retrieve the appropriate Axis object
        ax_for_querying, ax_not_for_querying = (
            (self.bc, self.ft)
            if flag_axis_for_querying_is_barcode
            else (self.ft, self.bc)
        )

        """ load the layer """
        if name_layer is not None:
            # handle invalid layer
            if name_layer not in self.layers:
                if self.verbose:
                    logger.error(f"the given layer '{name_layer}' does not exist")
                return
            self.layer = name_layer  # load the target layer
        else:  # by default, use the current layer
            if self.layer is None:
                if self.verbose:
                    logger.error(
                        f"no 'name_layer' argument was given but currently no layer is active, exiting."
                    )
                return

        """ load RAMtx """
        # retrieve appropriate rtx object
        rtx = self.layer.get_ramtx(
            flag_is_for_querying_features=not flag_axis_for_querying_is_barcode
        )
        # handle when appropriate RAMtx object does not exist
        if rtx is None:
            if self.verbose:
                logger.info(f"RAMtx appropriate for the given axis does not exist")
            return

        # parse query
        l_int_entry_query = BA.to_integer_indices(
            ax_for_querying[queries]
        )  # retrieve bitarray of the queried entries, convert to list of integer indices

        if flag_using_cluster_label_for_retrieving_mask:
            """
            % cluster based subsampling
            """
            if (
                name_col_label not in ax_not_for_querying.meta
            ):  # if the metadata column containing the label does not exist, exit
                if self.verbose:
                    logger.error(
                        f"the metadata column '{name_col_label}' does not exist, exiting"
                    )
                return

            """ retrieve labels """
            # retrieve the number of entries for each category
            (
                dict_cat_to_l_index,
                dict_cat_count,
            ) = ax_not_for_querying.meta.map_category_to_entries(
                name_col=name_col,
                flag_use_integer_representation_of_category=True,
                flag_return_dict_cat_to_num_entries=True,
            )

            ax_not_for_querying.meta.load_as_dict(
                name_col_label, flag_retrieve_categorical_data_as_integers=True
            )
            dict_cat = ax_not_for_querying.meta.dict[name_col_label]
        """ retrieve expressions """
        ax_not_for_querying.backup_view()  # back-up current view and reset the view of the axis not for querying
        if flag_retrieve_mask:
            ba_filter = (
                ax_not_for_querying.all(
                    flag_return_valid_entries_in_the_currently_active_layer=False
                )
                if flag_AND_operation
                else ax_not_for_querying.none()
            )  # default mask is 'all' for AND operation and 'none' for OR operation
            for (
                int_entry_of_axis_for_querying,
                arr_int_entry_of_axis_not_for_querying,
                arr_value,
            ) in zip(
                *rtx[l_int_entry_query]
            ):  # iterate over each entry
                mask = arr_value >= float_min_expr
                arr_int_entry_of_axis_not_for_querying_filtered = arr_int_entry_of_axis_not_for_querying[
                    mask
                ]  # filter 'int_entry_of_axis_not_for_querying_filtered' based on the expression

                if flag_using_cluster_label_for_retrieving_mask:
                    """
                    % cluster based subsampling
                    """
                    ba = (
                        ax_not_for_querying.none()
                    )  # initialize bitarray filter of the current entry
                    dict_cat_count_for_current_entry = bk.COUNTER(
                        list(
                            dict_cat[int_entry]
                            for int_entry in arr_int_entry_of_axis_not_for_querying_filtered
                        )
                    )  # retrieve 'dict_cat_count_for_current_entry' for the current entry of the axis for querying
                    for cat in dict_cat_count:  # for each category
                        if (
                            float_min_prop_in_a_label
                            <= (
                                dict_cat_count_for_current_entry[cat]
                                if cat in dict_cat_count_for_current_entry
                                else 0
                            )
                            / dict_cat_count[cat]
                        ):  # if the current category satisfy the threshold of the minimum proportion of active entries, include all entries of the current category for the current filter
                            for index in dict_cat_to_l_index[
                                cat
                            ]:  # for each entry of the selected category
                                ba[
                                    index
                                ] = True  # include entry of the selected category in the filter

                else:
                    ba = ax_not_for_querying._convert_to_bitarray(
                        arr_int_entry_of_axis_not_for_querying_filtered
                    )  # use the active entries in the filter

                """ update the filter using the filter from the current entry """
                if flag_AND_operation:
                    ba_filter &= ba
                else:
                    ba_filter |= ba
        else:
            mtx = rtx.get_sparse_matrix(
                l_int_entry_query
            )  # retrieve expr matrix of the queries in sparse format
            arr_expr = np.array(
                (
                    mtx[l_int_entry_query]
                    if flag_axis_for_querying_is_barcode
                    else mtx[:, l_int_entry_query].T
                ).sum(axis=0)
            )[
                0
            ]  # retrieve summarized expression values of the queried entries # convert it to numpy array of shape (len_axis_not_for_querying, )
        ax_not_for_querying.restore_view()  # restore view

        """ save result as a column """
        if (
            name_new_col is not None
        ):  # if valid 'name_new_col' column name has been given, save the retrieved data as a metadata column
            if flag_retrieve_mask:
                ax_not_for_querying.save_as_filter(
                    ba_filter, name_new_col
                )  # save a filter
            else:
                ax_not_for_querying.meta[
                    name_new_col, :
                ] = arr_expr  # save expression values
        return (
            ba_filter if flag_retrieve_mask else arr_expr
        )  # return retrieved expression values or mask of active entries

    """ memory-efficient PCA """

    def train_pca(
        self,
        name_model="ipca",
        name_layer="normalized_log1p_capped",
        int_num_components=50,
        axis: Union[int, str] = "barcodes",
        int_num_barcodes_in_ipca_batch=50000,
        name_col_filter="filter_pca",
        float_prop_subsampling=1,
        name_col_filter_subsampled="filter_pca_subsampled",
        flag_ipca_whiten=False,
        int_num_threads=3,
        flag_show_graph=True,
        int_index_component_reference: Union[None, int] = None,
    ):
        """# 2023-04-03 18:23:02
        Perform incremental PCA in a very memory-efficient manner.
        the resulting incremental PCA model will be saved in the RamData models database.

        arguments:
        'name_model' : the trained incremental PCA model will be saved to RamData models database with this name. if None is given, the model will not be saved. If model already exists, the model will be updated with new training data. If model is given, 'name_layer' and 'axis' arguments are optional.
        'name_layer' : name of the data source layer (the layer from which gene expression data will be retrieved for the barcodes)
        'name_col' : 'name_col' of the PCA data that will be added to Axis.meta ZDF.
        'name_col_filter' : the name of 'feature'/'barcode' Axis metadata column to retrieve selection filter for highly-variable-features. (default: None) if None is given, current feature filter (if it has been set) will be used as-is. if a valid filter is given, filter WILL BE CHANGED.
        'name_col_filter_subsampled' : the name of 'feature'/'barcode' Axis metadata column to retrieve or save mask containing subsampled barcodes. if 'None' is given and 'float_prop_subsampling' is below 1 (i.e. subsampling will be used), the subsampling filter generated for retrieving gene expression data of selected barcodes will not be saved.
        'int_num_components' : number of PCA components.
        'int_num_barcodes_in_ipca_batch' : number of barcodes in an Incremental PCA computation
        'float_prop_subsampling' : proportion of barcodes to used to train representation of single-barcode data using incremental PCA. 1 = all barcodes, 0.1 = 10% of barcodes, etc. subsampling will be performed using a random probability, meaning the actual number of barcodes subsampled will not be same every time.
        'flag_ipca_whiten' : a flag for an incremental PCA computation (Setting this flag to 'True' will reduce the efficiency of model learning, but might make the model more generalizable)
        'int_num_threads' : number of threads for parallel data retrieval/iPCA transformation/ZarrDataFrame update. 3~5 would be ideal. should be larger than 2
        'axis' : Union[ int, str ] = 'barcodes' # axis representing samples or 'points'. the other axis will represents the features of the 'points'
        'flag_show_graph' : show graph

        === when reference ramdata is used ===
        int_index_component_reference : Union[ None, int ] = None # the index of the reference component RamData to use. if None is given, does not use any component as a reference component
        """
        from sklearn.decomposition import IncrementalPCA

        """
        1) Prepare
        """
        """
        # load model
        """
        # initialize the model
        # check whether the model already exist
        model = self.load_model(name_model, "ipca")
        if model is None:
            if self.verbose:
                logger.error(
                    f"iPCA model '{name_model}' does not exist in the RamData models database, initializing the model."
                )
            # initialize iPCA object
            ipca = IncrementalPCA(
                n_components=int_num_components,
                batch_size=int_num_barcodes_in_ipca_batch,
                copy=False,
                whiten=flag_ipca_whiten,
            )  # copy = False to increase memory-efficiency

            # handle inputs
            flag_axis_is_barcode = self._determine_axis(
                axis
            )  # retrieve a flag indicating whether the data is summarized for each barcode or not
        else:
            if self.verbose:
                logger.info(
                    f"existing iPCA model '{name_model}' found. the model will be updated using the currently defined inputs."
                )
            # parse the model
            ipca = model["ipca"]
            flag_axis_is_barcode = model["flag_axis_is_barcode"]
            int_num_components = model["int_num_components"]
            int_num_barcodes_in_ipca_batch = model["int_num_barcodes_in_ipca_batch"]
            flag_ipca_whiten = model["flag_ipca_whiten"]
            arr_features_str_0 = model["arr_features_str_0"]
            arr_features_str_1 = model["arr_features_str_1"]
            ba_filter_of_axis_features = model["filter_of_axis_features"]
            identifier = model["identifier"]
            if name_layer is None:  # retrieve the default 'name_layer'
                name_layer = model["name_layer"]

            # handle inputs
            if axis is not None:  # set default axis
                flag_axis_is_barcode = self._determine_axis(
                    axis
                )  # retrieve a flag indicating whether the data is summarized for each barcode or not # override settings from the loaded model

        """
        # load layer, axis, and RAMtx
        """
        # set default 'index_component_reference'
        if self.is_combined:
            if int_index_component_reference is None:
                int_index_component_reference = self.int_index_component_reference
        else:
            int_index_component_reference = None

        # load layer
        if name_layer not in self.layers:
            if self.verbose:
                logger.info(
                    f"[ERROR] [RamData.apply_pca] invalid argument 'name_layer' : '{name_layer}' does not exist."
                )
            return -1
        # set layer
        self.layer = name_layer

        # retrieve an RamDataAxis and RAMtx object (sorted by barcodes/features) to summarize
        ax, ax_features = (
            (self.bc, self.ft) if flag_axis_is_barcode else (self.ft, self.bc)
        )  # retrieve the Axis objects according to their roles

        rtx = self.layer.get_ramtx(
            flag_is_for_querying_features=not flag_axis_is_barcode
        )
        if rtx is None:
            if self.verbose:
                logger.info(
                    f"[ERROR] [RamData.train_pca] valid ramtx object is not available in the '{self.layer.name}' layer"
                )

        # set/save filter
        if name_col_filter is not None:
            self.change_or_save_filter(name_col_filter)

        # set 'observation' filters excluding 'observation' from the reference
        if int_index_component_reference is not None:
            ba_filter_all_components = (
                ax.filter
            )  # backup the filter before modifying the filter
            ax.filter = (ax.all() if ax.filter is None else ax.filter) & (
                ~ax.select_component(int_index_component_reference)
            )  # exclude entries of the reference component

        # create view for 'feature' Axis
        ax_features.create_view(
            index_component=int_index_component_reference
        )  # create view if the reference component is used
        # change component if reference component is used
        ax_features.set_destination_component(
            int_index_component_reference
        )  # change coordinates to match that of the component if the reference component is used

        # retrieve a flag indicating whether a subsampling is active
        flag_is_subsampling_active = (name_col_filter_subsampled in ax.meta) or (
            float_prop_subsampling is not None and float_prop_subsampling < 1
        )  # perform subsampling if 'name_col_filter_subsampled' is valid or 'float_prop_subsampling' is below 1

        # if a subsampling is active, retrieve a filter containing subsampled 'observation' and apply the filter to the 'observation' Axis
        if flag_is_subsampling_active:
            # retrieve 'observation' filter before subsampling
            ba_filter_bc_before_subsampling = ax.filter

            # set 'observation' filter after subsampling
            if (
                name_col_filter_subsampled in ax.meta
            ):  # if 'name_col_filter_subsampled' 'observation' filter is available, load the filter
                ax.change_filter(name_col_filter_subsampled)
            else:  # if the 'name_col_filter_subsampled' 'observation' filter is not available, build a filter containing subsampled entries and save the filter
                ax.filter = ax.subsample(float_prop_subsampling=float_prop_subsampling)
                ax.save_filter(name_col_filter_subsampled)

        # create view for 'barcode' Axis
        ax.create_view()

        """
        2) Fit PCA with/without subsampling of barcodes
        """

        # define functions for multiprocessing step
        def process_batch(pipe_receiver_batch, pipe_sender_result):
            """# 2022-09-20 11:51:39
            prepare data as a sparse matrix for the batch
            """
            # retrieve fork-safe RAMtx
            rtx_fork_safe = (
                rtx.get_fork_safe_version() if rtx.contains_remote else rtx
            )  # load zarr_server (if RAMtx contains remote data source) to be thread-safe

            while True:
                batch = pipe_receiver_batch.recv()
                if batch is None:
                    break
                # parse the received batch
                int_num_of_previously_returned_entries, l_int_entry_current_batch = (
                    batch["int_num_of_previously_returned_entries"],
                    batch["l_int_entry_current_batch"],
                )
                int_num_retrieved_entries = len(l_int_entry_current_batch)

                pipe_sender_result.send(
                    (
                        int_num_of_previously_returned_entries,
                        int_num_retrieved_entries,
                        rtx_fork_safe.get_sparse_matrix(l_int_entry_current_batch)[
                            int_num_of_previously_returned_entries : int_num_of_previously_returned_entries
                            + int_num_retrieved_entries
                        ],
                    )
                )  # retrieve and send sparse matrix as an input to the incremental PCA # resize sparse matrix
            # destroy zarr servers
            rtx_fork_safe.terminate_spawned_processes()

        pbar = progress_bar(
            desc=f"{int_num_components} PCs from {len( ax_features.meta )} features",
            total=ax.meta.n_rows,
        )  # initialize the progress bar

        def post_process_batch(res):
            """# 2022-07-13 22:18:18
            perform partial fit for batch
            """
            (
                int_num_of_previously_returned_entries,
                int_num_retrieved_entries,
                X,
            ) = res  # parse the result
            try:
                ipca.partial_fit(
                    X.toarray()
                )  # perform partial fit using the retrieved data # partial_fit only supports dense array
            except (
                ValueError
            ):  # handles 'ValueError: n_components=50 must be less or equal to the batch number of samples 14.' error # 2022-07-18 15:09:52
                if self.verbose:
                    logger.info(
                        f"current batch contains less than {int_num_components} number of barcodes, which is incompatible with iPCA model. therefore, current batch will be skipped."
                    )
            pbar.update(
                int_num_retrieved_entries
            )  # update the progress bar once the training has been completed

            if self.verbose:  # report
                logger.info(
                    f"fit completed for {int_num_of_previously_returned_entries + 1}-{int_num_of_previously_returned_entries + int_num_retrieved_entries} barcodes"
                )

        # fit iPCA using multiple processes
        bk.Multiprocessing_Batch_Generator_and_Workers(
            ax.batch_generator(
                int_num_entries_for_batch=int_num_barcodes_in_ipca_batch
            ),
            process_batch,
            post_process_batch=post_process_batch,
            int_num_threads=max(int_num_threads, 2),
            int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
        )  # number of threads for multi-processing is 2 ~ 5 # generate batch with fixed number of barcodes
        pbar.close()  # close the progress bar

        # report
        if self.verbose:
            logger.info("fit completed")
        # fix error of ipca object
        if not hasattr(ipca, "batch_size_"):
            ipca.batch_size_ = (
                ipca.batch_size
            )  # 'batch_size_' attribute should be set for 'transform' method to work..

        # if subsampling has been completed, revert to the original barcode selection filter
        if flag_is_subsampling_active:
            ax.filter = ba_filter_bc_before_subsampling
            del ba_filter_bc_before_subsampling

        # destroy the view
        self.destroy_view()
        ax_features.set_destination_component(
            None
        )  # reset destination component (the output will represent coordinates of combined axis)

        # compose and save the model
        model = {
            "ipca": ipca,
            "name_layer": name_layer,
            "flag_axis_is_barcode": flag_axis_is_barcode,
            "int_num_components": int_num_components,
            "int_num_barcodes_in_ipca_batch": int_num_barcodes_in_ipca_batch,
            "flag_ipca_whiten": flag_ipca_whiten,
            "arr_features_str_0": ax_features.load_str(
                int_index_col=0, flag_load_without_updating_mapping=True
            ),  # retrieve string representations
            "arr_features_str_1": ax_features.load_str(
                int_index_col=1, flag_load_without_updating_mapping=True
            ),  # retrieve string representations
            "filter_of_axis_features": ax_features.filter,
            "identifier": self.identifier,
        }
        if name_model is not None:  # if the given 'name_model' is valid
            self.save_model(model, name_model, "ipca")  # save model

        # reset barcode filter
        if int_index_component_reference is not None:
            ax.filter = (
                ba_filter_all_components  # restore the filter before modification
            )

        # draw graphs
        if flag_show_graph:
            # draw 'explained variance ratio' graph
            fig, ax = plt.subplots(1, 1)
            ax.plot(ipca.explained_variance_ratio_, "o-")
            bk.MATPLOTLIB_basic_configuration(
                x_label="principal components",
                y_label="explained variance ratio",
                title="PCA result",
                show_grid=True,
            )

        return model  # return the model

    def apply_pca(
        self,
        name_model="ipca",
        name_col="X_pca",
        int_n_components_in_a_chunk=20,
        name_layer: Union[None, str] = None,
        name_col_filter: Union[str, None] = None,
        axis: Union[None, int, str] = None,
        int_num_threads=5,
        int_index_component_reference: Union[None, int] = None,
    ):
        """# 2023-02-21 13:27:34
        Apply trained incremental PCA in a memory-efficient manner.

        arguments:
        'name_model' : the trained incremental PCA model will be saved to RamData.ns database with this name. if None is given, the model will not be saved.
        name_layer : Union[ None, str ] = None, # name of the data source layer (the layer from which gene expression data will be retrieved for the barcodes). By default, the name of the layer recorded in the loaded model will be used.
        'name_col' : 'name_col' of the PCA data that will be added to Axis.meta ZDF.
        name_col_filter : Union[ str, None ] = None, # the name of 'feature'/'barcode' Axis metadata column to retrieve selection filter for highly-variable-features. (default: None) if None is given, By default, the filter object (if it belongs to the current RamData object) or string representations of the features saved with the loaded model will be used. if a valid filter is given, filter of the current object WILL BE CHANGED.
        axis : Union[ None, int, str ] = None, # the axis of the 'observation' to which the loaded model will be applied. By default, the axis selection recorded in the loaded model will be used.

        'int_n_components_in_a_chunk' : deterimines the chunk size for PCA data store
        'int_num_threads' : the number of threads to use for parellel processing. the larger the number of threads are, the larger memory consumed by all the workers.

        === when reference ramdata is used ===
        int_index_component_reference : Union[ None, int ] = None # the index of the reference component RamData to use. By default, 'index_component_reference' attribute of the current RamData will be used.
        """
        """
        1) Load Model and Prepare
        """
        # exit if the model does not exist
        model = self.load_model(name_model, "ipca")
        if model is None:
            if self.verbose:
                logger.error(
                    f"iPCA model '{name_model}' does not exist in the RamData models database"
                )
            return

        # parse the model
        ipca = model["ipca"]
        flag_axis_is_barcode = model["flag_axis_is_barcode"]
        int_num_components = model["int_num_components"]
        int_num_barcodes_in_ipca_batch = model["int_num_barcodes_in_ipca_batch"]
        flag_ipca_whiten = model["flag_ipca_whiten"]
        arr_features_str_0 = model["arr_features_str_0"]
        arr_features_str_1 = model["arr_features_str_1"]
        ba_filter_of_axis_features = model["filter_of_axis_features"]
        identifier = model["identifier"]
        if name_layer is None:  # retrieve the default 'name_layer'
            name_layer = model["name_layer"]

        # check the validility of the input arguments
        if name_layer not in self.layers:
            if self.verbose:
                logger.info(
                    f"[ERROR] [RamData.apply_pca] invalid argument 'name_layer' : '{name_layer}' does not exist."
                )
            return -1
        # set layer
        self.layer = name_layer

        # handle inputs
        if axis is not None:  # set default axis
            flag_axis_is_barcode = self._determine_axis(
                axis
            )  # retrieve a flag indicating whether the data is summarized for each barcode or not # override settings from the loaded model

        # retrieve an RamDataAxis and RAMtx object (sorted by barcodes/features) to summarize
        ax, ax_features = (
            (self.bc, self.ft) if flag_axis_is_barcode else (self.ft, self.bc)
        )  # retrieve the Axis objects according to their roles

        rtx = self.layer.get_ramtx(
            flag_is_for_querying_features=not flag_axis_is_barcode
        )
        if rtx is None:
            if self.verbose:
                logger.info(
                    f"[ERROR] [RamData.train_pca] valid ramtx object is not available in the '{self.layer.name}' layer"
                )

        # set default 'index_component_reference'
        if self.is_combined:
            if int_index_component_reference is None:
                int_index_component_reference = self.int_index_component_reference
        else:
            int_index_component_reference = None

        # set filters
        l_entry_view = None  # does not use string representations by default
        if name_col_filter is not None:  # if 'name_col_filter' has been given
            self.change_filter(name_col_filter)
        else:  # use default filters from the loaded model
            if (
                self.identifier == identifier
            ):  # if the model originated from the current RamData
                ax_features.filter = (
                    ba_filter_of_axis_features  # use the filter saved with the model
                )
            else:  # if the model did not originated from the currenr RamData, attempts to retrieve filter from the current axis using the string representations of the entries
                l_entry_view = (
                    arr_features_str_0  # use for 'arr_features_str_0' creating a view
                )
                ax_features.load_str(
                    int_index_col=0
                )  # load string representations of column 0
                ax_features.filter = ax_features[
                    l_entry_view
                ]  # set the filter using the given list of string representations saved with the model

        # set barcode filters excluding barcodes from the reference
        if int_index_component_reference is not None:
            ba_filter_all_components = (
                ax.filter
            )  # backup the filter before modifying the filter
            ax.filter = (ax.all() if ax.filter is None else ax.filter) & (
                ~ax.select_component(int_index_component_reference)
            )  # exclude entries of the reference component

        # create view of the RamData
        ax_features.create_view(
            index_component=int_index_component_reference,
            l_entry_view=l_entry_view,
            int_index_str_rep=0,
        )
        ax.create_view()
        # change component if reference component is used
        ax_features.set_destination_component(
            int_index_component_reference
        )  # change coordinates to match that of the component if the reference component is used

        # prepare pca column in the metadata
        ax.meta.initialize_column(
            name_col,
            dtype=np.float64,
            shape_not_primary_axis=(ipca.n_components,),
            chunks=(int_n_components_in_a_chunk,),
            categorical_values=None,
        )  # initialize column

        """
        2) Transform Data
        """

        # define functions for multiprocessing step
        def process_batch(pipe_receiver_batch, pipe_sender_result):
            """# 2022-09-06 17:05:15
            retrieve data and retrieve transformed PCA values for the batch
            """
            # retrieve fork-safe RAMtx
            rtx_fork_safe = (
                rtx.get_fork_safe_version() if rtx.contains_remote else rtx
            )  # load zarr_server (if RAMtx contains remote data source) to be thread-safe

            while True:
                batch = pipe_receiver_batch.recv()
                if batch is None:
                    break
                # parse the received batch
                (
                    int_num_processed_records,
                    int_num_of_previously_returned_entries,
                    l_int_entry_current_batch,
                ) = (
                    batch["int_accumulated_weight_current_batch"],
                    batch["int_num_of_previously_returned_entries"],
                    batch["l_int_entry_current_batch"],
                )
                int_num_retrieved_entries = len(l_int_entry_current_batch)

                pipe_sender_result.send(
                    (
                        int_num_processed_records,
                        l_int_entry_current_batch,
                        rtx_fork_safe.get_sparse_matrix(l_int_entry_current_batch)[
                            int_num_of_previously_returned_entries : int_num_of_previously_returned_entries
                            + int_num_retrieved_entries
                        ],
                    )
                )  # retrieve data as a sparse matrix and send the result of PCA transformation # send the integer representations of the barcodes for PCA value update

        (
            pipe_sender,
            pipe_receiver,
        ) = (
            mp.Pipe()
        )  # create a communication link between the main process and the worker for saving zarr objects
        pbar = progress_bar(
            desc=f"{ipca.n_components} PCs from {len( ax_features.meta )} features",
            total=rtx.get_total_num_records(
                int_num_entries_for_each_weight_calculation_batch=self.int_num_entries_for_each_weight_calculation_batch,
                flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=self.flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx,
            ),
        )

        def post_process_batch(res):
            """# 2022-07-13 22:18:26
            perform PCA transformation for each batch
            """
            # parse result
            int_num_processed_records, l_int_entry_current_batch, X = res

            X_transformed = ipca.transform(X)  # perform PCA transformation
            del X

            pbar.update(int_num_processed_records)  # update the progress bar

            # send result to the worker
            pipe_sender.send(
                (int_num_processed_records, l_int_entry_current_batch, X_transformed)
            )

        # start the worker
        def __worker_for_saving_zarr(pipe_receiver):
            """# 2022-08-08 18:00:05
            save transformed PCA components to the metadata for each batch
            """
            while True:
                res = pipe_receiver.recv()
                # terminate if None is received
                if res is None:
                    break

                (
                    int_num_processed_records,
                    l_int_entry_current_batch,
                    X_transformed,
                ) = res  # parse the result

                # update the PCA components for the barcodes of the current batch
                ax.meta[name_col, l_int_entry_current_batch] = X_transformed

        p = mp.Process(target=__worker_for_saving_zarr, args=(pipe_receiver,))
        p.start()

        # transform values using iPCA using multiple processes
        bk.Multiprocessing_Batch_Generator_and_Workers(
            rtx.batch_generator(
                ax.filter,
                int_num_entries_for_each_weight_calculation_batch=self.int_num_entries_for_each_weight_calculation_batch,
                int_total_weight_for_each_batch=self.int_total_weight_for_each_batch,
                flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx=self.flag_use_total_number_of_entries_of_axis_not_for_querying_as_weight_for_dense_ramtx,
            ),
            process_batch,
            post_process_batch=post_process_batch,
            int_num_threads=int_num_threads,
            int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
        )
        pbar.close()  # close the progress bar
        # dismiss the worker
        pipe_sender.send(None)  # send the termination signal
        p.join()

        # destroy the view
        self.destroy_view()
        ax_features.set_destination_component()  # reset destination component (the output will represent coordinates of combined axis)

        # reset barcode filter
        if int_index_component_reference is not None:
            ax.filter = (
                ba_filter_all_components  # restore the filter before modification
            )
        return model

    """ memory-efficient UMAP """

    def train_umap(
        self,
        name_col_pca="X_pca",
        int_num_components_pca=20,
        int_num_components_umap=2,
        name_col_filter: Union[str, None] = "filter_umap",
        name_pumap_model="pumap",
        name_pumap_model_new: Union[str, None] = None,
        dict_kw_pumap: dict = {"metric": "euclidean"},
    ):
        """# 2022-08-07 11:13:38
        Perform Parametric UMAP to embed cells in reduced dimensions for a scalable analysis of single-cell data

        * Parametric UMAP has several advantages over non-parametric UMAP (conventional UMAP), which are
            (1) GPU can be utilized during training of neural network models
            (2) learned embedding can be applied to other cells not used to build the embedding
            (3) learned embedding can be updated by training with additional cells
        Therefore, parametric UMAP is suited for generating embedding of single-cell data with extremely large number of cells

        arguments:
        'name_col_pca' : 'name_col' of the columns containing PCA transformed values.
        'int_num_components_pca' : number of PCA components to use as inputs for Parametric UMAP learning
        'name_col_umap' : 'name_col' of the columns containing UMAP transformed values.
        'int_num_components_umap' : number of output UMAP components. (default: 2)
        'name_col_filter' : the name of 'feature'/'barcode' Axis metadata column to retrieve selection filter for highly-variable-features. (default: None) if None is given, current feature filter (if it has been set) will be used as-is. if a valid filter is given, filter WILL BE CHANGED.
        'name_pumap_model' = 'pumap' : the name of the parametric UMAP model. if None is given, the trained model will not be saved to the RamData object. if the model already exists, the model will be loaded and trained again.
        'name_pumap_model_new' = 'pumap' : the name of the new parametric UMAP model after the training. if None is given, the new model will not be saved. if 'name_pumap_model' and 'name_pumap_model_new' are the same, the previously written model will be overwritten.
        'dict_kw_pumap' : remaining keyworded arguments of umap.ParametricUMAP

        """
        import umap.parametric_umap as pumap  # parametric UMAP

        """
        1) Prepare
        """
        # handle arguments
        if name_pumap_model_new is None:
            name_pumap_model_new = name_pumap_model
        # retrieve 'Barcode' Axis object
        ax = self.bc

        # set/save filter
        if name_col_filter is not None:
            self.change_or_save_filter(name_col_filter)
        """
        2) Train Parametric UMAP 
        """
        # load pumap model
        pumap_embedder = self.load_model(name_pumap_model, "pumap")
        if pumap_embedder is None:
            pumap_embedder = pumap.ParametricUMAP(
                low_memory=True, n_components=int_num_components_umap, **dict_kw_pumap
            )  # load an empty model if a saved model is not available

        # train parametric UMAP model
        pumap_embedder.fit(self.bc.meta[name_col_pca, None, :int_num_components_pca])

        # report
        if self.verbose:
            logger.info(
                f"[Info] [RamData.train_umap] training for {ax.meta.n_rows} entries completed"
            )

        # save the model
        int_model_file_size = self.save_model(
            pumap_embedder, name_pumap_model_new, "pumap"
        )
        if int_model_file_size is not None:
            # report the file size of the model if saving of the model was successful
            if self.verbose:
                logger.info(
                    f"[Info] [RamData.train_umap] Parametric UMAP model of {int_model_file_size} Bytes has been saved."
                )
        return pumap_embedder  # return the model

    def apply_umap(
        self,
        name_col_pca: str = "X_pca",
        name_col_umap: str = "X_umap",
        int_num_barcodes_in_pumap_batch: int = 20000,
        name_col_filter: Union[str, None] = "filter_umap",
        name_pumap_model: Union[str, None] = "pumap",
    ):
        """# 2022-08-07 11:27:20
        Embed barcodes to lower-dimensional space using the trained Parametric UMAP in a scalable way

        * Parametric UMAP has several advantages over non-parametric UMAP (conventional UMAP), which are
            (1) GPU can be utilized during training of neural network models
            (2) learned embedding can be applied to other cells not used to build the embedding
            (3) learned embedding can be updated by training with additional cells
        Therefore, parametric UMAP is suited for generating embedding of single-cell data with extremely large number of cells

        arguments:
        'name_col_pca' : 'name_col' of the columns containing PCA transformed values.
        'name_col_umap' : 'name_col' of the columns containing UMAP transformed values.
        'int_num_barcodes_in_pumap_batch' : number of barcodes in a batch for Parametric UMAP model update.
        'name_col_filter' : the name of 'feature'/'barcode' Axis metadata column to retrieve selection filter for highly-variable-features. (default: None) if None is given, current feature filter (if it has been set) will be used as-is. if a valid filter is given, filter WILL BE CHANGED.
        'name_pumap_model' = 'pumap' : the name of the parametric UMAP model. if None is given, the trained model will not be saved to the RamData object. if the model already exists, the model will be loaded and trained again.
        """
        """
        1) Prepare
        """
        # # retrieve 'Barcode' Axis object
        ax = self.bc

        # set filters
        if name_col_filter is not None:
            self.change_filter(name_col_filter)

        # load the model
        pumap_embedder = self.load_model(name_pumap_model, "pumap")  # load the model
        if pumap_embedder is None:
            if self.verbose:
                logger.error(
                    f"[RamData.apply_umap] the parametric UMAP model {name_pumap_model} does not exist in the current RamData, exiting"
                )
            return
        # retrieve the number of pca components for the input of pumap model
        int_num_components_pca = pumap_embedder.dims[0]
        if (
            ax.meta.get_shape(name_col_pca)[0] < int_num_components_pca
        ):  # check compatibility between the given PCA data and the given pumap model # if the number of input PCA components is larger than the components available in the input PCA column, exit
            if self.verbose:
                logger.error(
                    f"[RamData.apply_umap] the number of PCA components of the given parametric UMAP model {name_pumap_model} is {int_num_components_pca}, which is larger than the number of PCA components available in {name_col_pca} data in the 'barcode' metadata, exiting"
                )
            return

        """
        2) Transform Data
        """
        pbar = progress_bar(
            desc=f"pUMAP", total=ax.meta.n_rows
        )  # initialize the progress bar
        # iterate through batches
        for batch in ax.batch_generator(
            int_num_entries_for_batch=int_num_barcodes_in_pumap_batch
        ):
            l_int_entry_current_batch = batch[
                "l_int_entry_current_batch"
            ]  # parse batch
            int_num_retrieved_entries = len(
                l_int_entry_current_batch
            )  # retrieve the number of retrieve entries
            pbar.update(int_num_retrieved_entries)  # update the progress bar

            # retrieve UMAP embedding of barcodes of the current batch
            X_transformed = pumap_embedder.transform(
                self.bc.meta[
                    name_col_pca, l_int_entry_current_batch, :int_num_components_pca
                ]
            )

            # update the components for the barcodes of the current batch
            ax.meta[name_col_umap, l_int_entry_current_batch] = X_transformed
        pbar.close()  # close the progress bar

        return pumap_embedder  # return the model

    """ for community detection """

    def hdbscan(
        self,
        name_model: str = "hdbscan",
        name_col_data: str = "X_umap",
        int_num_components_data: int = 2,
        name_col_label: str = "hdbscan",
        min_cluster_size: int = 30,
        min_samples: int = 30,
        cut_distance: float = 0.15,
        flag_reanalysis_of_previous_clustering_result: bool = False,
        name_col_filter: Union[str, None] = "filter_hdbscan",
        name_col_embedding: Union[str, None] = None,
        dict_kw_scatter: dict = {"s": 10, "linewidth": 0, "alpha": 0.05},
        index_col_of_name_col_label: Union[int, None] = None,
    ):
        """# 2022-08-09 02:19:26
        Perform HDBSCAN for the currently active barcodes

        arguments:
        'name_model' : name of the model saved/will be saved in RamData.models database. if the model already exists, 'cut_distance' and 'min_cluster_size' arguments will become active.

        === data input ===
        'name_col_data' : 'name_col' of the column containing data. UMAP embeddings are recommended (PCA data is not recommended as an input to HDBSCAN clustering, since it is much more sparse and noisy than UMAP embedded data)
        'int_num_components_data' : number of components of the data for clustering (default: 2)

        === clustering arguments ===
        'min_cluster_size', 'min_samples' : arguments for HDBSCAN method. please refer to the documentation of HDBSCAN (https://hdbscan.readthedocs.io/)
        'cut_distance' and 'min_cluster_size' : arguments for the re-analysis of the clustering result for retrieving more fine-grained/coarse-grained cluster labels (for more info., please refer to hdbscan.HDBSCAN.single_linkage_tree_.get_clusters docstring).
        'flag_reanalysis_of_previous_clustering_result' : if 'flag_reanalysis_of_previous_clustering_result' is True and 'name_model' exists in the RamData.ns database, use the hdbscan model saved in the database to re-analyze the previous hierarchical DBSCAN clustering result. 'cut_distance' and 'min_cluster_size' arguments can be used to re-analyze the clustering result and retrieve more fine-grained/coarse-grained cluster labels (for more info., please refer to hdbscan.HDBSCAN.single_linkage_tree_.get_clusters docstring). To perform hdbscan from the start, change name_model to a new name or delete the model from RamData.ns database

        === output ===
        'name_col_label' : 'name_col' of the axis metadata that will contain cluster labels assigned by the current clustering algorithm
        'index_col_of_name_col_label' : index of the secondary axis of the column of 'name_col_label' that will contain cluster labels. if None, 'name_col_label' is assumed to be a 1-dimensional column.

        === cell filter ===
        'name_col_filter' : the name of 'feature'/'barcode' Axis metadata column to retrieve selection filter for running the current method. if None is given, current barcode/feature filters (if it has been set) will be used as-is.

        === settings for drawing graph ===
        'name_col_embedding' : 'name_col' of the column containing the embeddings for the visualization of the clustering results. if None is given, the graph will not be drawn
        'dict_kw_scatter' : arguments for 'matplotlib Axes.scatter' that will be used for plotting

        returns:
        arr_cluster_label, clusterer(hdbscan object)
        """
        import hdbscan  # for clustering

        """
        1) Prepare
        """
        # # retrieve 'Barcode' Axis object
        ax = self.bc

        # set filters for operation
        if name_col_filter is not None:
            self.change_or_save_filter(name_col_filter)

        """
        2) Train model and retrieve cluster labels
        """
        # load the model and retrieve cluster labels
        type_model = "hdbscan"
        clusterer = self.load_model(name_model, type_model)
        if clusterer is None:  # if the model does not exist, initiate the model
            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=min_cluster_size, min_samples=min_samples
            )  # initiate the model
            clusterer.fit(
                self.bc.meta[name_col_data, None, :int_num_components_data]
            )  # retrieve data # clustering embedded barcodes
            arr_cluster_label = clusterer.labels_  # retrieve cluster labels
            # save trained model
            if name_model is not None:  # check validity of 'name_model'
                self.save_model(
                    clusterer, name_model, type_model
                )  # save model to the RamData
        else:  # if 'name_model' hdbscan model exists in the database, use the previously computed clustering results
            if (
                flag_reanalysis_of_previous_clustering_result
            ):  # if 'flag_reanalysis_of_previous_clustering_result' is True, perform re-analysis of the clustering result
                arr_cluster_label = clusterer.single_linkage_tree_.get_clusters(
                    cut_distance=cut_distance, min_cluster_size=min_cluster_size
                )  # re-analyze previous clustering result, and retrieve cluster labels
            else:
                arr_cluster_label = (
                    clusterer.labels_
                )  # retrieve previously calculated cluster labels

        """
        3) save labels
        """
        if (
            index_col_of_name_col_label is None
        ):  # assume 'name_col_label' is 1-dimensional column
            # update all columns
            ax.meta[name_col_label] = arr_cluster_label
        else:
            # update a single column in the meatadata column 'name_col_label'
            ax.meta[
                name_col_label, None, index_col_of_name_col_label
            ] = arr_cluster_label

        # report
        if self.verbose:
            logger.info(
                f"[Info] [RamData.hdbscan] clustering completed for {ax.meta.n_rows} number of barcodes"
            )

        # draw graphs
        if (
            name_col_embedding is not None
        ):  # visualize clustering results if 'name_col_embedding' has been given
            import seaborn as sns

            color_palette = sns.color_palette("Paired", len(set(arr_cluster_label)))
            cluster_colors = [
                color_palette[x] if x >= 0 else (0.5, 0.5, 0.5)
                for x in arr_cluster_label
            ]
            fig, plt_ax = plt.subplots(1, 1, figsize=(7, 7))
            plt_ax.scatter(
                *self.bc.meta[name_col_embedding, None, :2].T,
                c=cluster_colors,
                **dict_kw_scatter,
            )  # retrieve embedding data and draw the graph

        # return results
        return (
            arr_cluster_label,
            clusterer,
        )  # return the trained model and computed cluster labels

    def leiden(
        self,
        name_model: str = "leiden",
        name_col_data: str = "X_pca",
        int_num_components_data: int = 15,
        name_col_label: str = "leiden",
        resolution: float = 0.2,
        int_num_clus_expected: Union[int, None] = None,
        directed: bool = True,
        use_weights: bool = True,
        dict_kw_leiden_partition: dict = {"n_iterations": -1, "seed": 0},
        dict_kw_pynndescent_transformer: dict = {
            "n_neighbors": 10,
            "metric": "euclidean",
            "low_memory": True,
        },
        name_col_filter: Union[str, None] = "filter_leiden",
        name_col_embedding: Union[str, None] = None,
        dict_kw_scatter: dict = {"s": 10, "linewidth": 0, "alpha": 0.05},
        index_col_of_name_col_label: Union[int, None] = None,
    ) -> None:
        """# 2022-08-09 02:19:31
        Perform leiden community detection algorithm (clustering) for the currently active barcodes

        arguments:
        'name_model' : name of the model saved/will be saved in RamData.models database. if the model already exists, 'cut_distance' and 'min_cluster_size' arguments will become active.

        === data input ===
        'name_col_data' : 'name_col' of the column containing data. PCA data is recommended.
        'int_num_components_data' : number of components of the data for clustering (default: 2)

        === output ===
        'name_col_label' : 'name_col' of the axis metadata that will contain cluster labels assigned by the current clustering algorithm
        'index_col_of_name_col_label' : index of the secondary axis of the column of 'name_col_label' that will contain cluster labels. if None, 'name_col_label' is assumed to be a 1-dimensional column.

        === clustering arguments ===
        'resolution' : initial resolution of cluster. please refer to 'resolution_parameter' of 'leidenalg.find_partition' method
        'int_num_clus_expected' : the expected number of clusters in the data to optimize hyperparameters for community detection. if 'int_num_clus_expected' is not None, until the number of detected communities reaches 'int_num_clus_expected', the 'resolution' parameter will be optimized. this argument will be inactive when 'resolution' is None.
        'directed' : create directed graph. it is recommended to set it to True
        'use_weights' : use weights of the kNN graph for the leiden partitioning
        'dict_kw_leiden_partition' : a dictionary containing keyworded arguments for the 'leidenalg.find_partition' method
        'dict_kw_pynndescent_transformer' : a dictionary containing keyworded arguments for the 'pynndescent.PyNNDescentTransformer' method for constructing kNN graph from the data

        === cell filter ===
        'name_col_filter' : the name of 'feature'/'barcode' Axis metadata column to retrieve selection filter for running the current method. if None is given, current barcode/feature filters (if it has been set) will be used as-is.

        === settings for drawing graph ===
        'name_col_embedding' : 'name_col' of the column containing the embeddings for the visualization of the clustering results. if None is given, the graph will not be drawn
        'dict_kw_scatter' : arguments for 'matplotlib Axes.scatter' that will be used for plotting

        returns:
        """
        # for leiden clustering
        import igraph as ig
        import leidenalg
        import pynndescent

        """
        1) Prepare
        """
        # # retrieve 'Barcode' Axis object
        ax = self.bc

        # set filters for operation
        if name_col_filter is not None:
            self.change_or_save_filter(name_col_filter)

        """
        2) construct kNN graph
        """
        # load the knn graph
        type_model = "knngraph"
        conn = self.load_model(name_model, type_model)
        if conn is None:  # if the knngraph does not exist, calculate the knngraph
            knnmodel = pynndescent.PyNNDescentTransformer(
                **dict_kw_pynndescent_transformer
            )
            conn = knnmodel.fit_transform(
                ax.meta[name_col_data, None, :int_num_components_data]
            )

            # save calculated knngraph
            if name_model is not None:  # check validity of 'name_model'
                self.save_model(
                    conn, name_model, type_model
                )  # save knngraph to the RamData

        """
        3) perform leiden clustering
        """

        # construct an igraph object from the knn graph
        def get_igraph_from_adjacency(adjacency, directed=None):
            """# 2022-08-09 02:28:09
            Get igraph graph from adjacency matrix.
            this code is mostly a copy of a function implemented in scanpy 'https://github.com/scverse/scanpy/blob/536ed15bc73ab5d1131c0d530dd9d4f2dc9aee36/scanpy/_utils/__init__.py'
            """
            import igraph as ig

            sources, targets = adjacency.nonzero()
            weights = adjacency[sources, targets]
            if isinstance(weights, np.matrix):
                weights = weights.A1
            g = ig.Graph(directed=directed)
            g.add_vertices(adjacency.shape[0])  # this adds adjacency.shape[0] vertices
            g.add_edges(list(zip(sources, targets)))
            try:
                g.es["weight"] = weights
            except KeyError:
                pass
            if g.vcount() != adjacency.shape[0]:
                if self.verbose:
                    logger.info(
                        f"The constructed graph has only {g.vcount( )} nodes. Your adjacency matrix contained redundant nodes."
                    )
            return g

        g = get_igraph_from_adjacency(conn, directed)
        del conn
        if self.verbose:
            logger.info(f"[Info] [RamData.leiden] knn-graph loaded")

        # compose partition arguments
        if resolution is not None:
            dict_kw_leiden_partition["resolution_parameter"] = resolution
        if use_weights:
            dict_kw_leiden_partition["weights"] = np.array(g.es["weight"]).astype(
                np.float64
            )

        while True:
            # perform leiden clustering
            arr_cluster_label = np.array(
                leidenalg.find_partition(
                    g,
                    leidenalg.RBConfigurationVertexPartition,
                    **dict_kw_leiden_partition,
                ).membership
            )

            # until the desired
            if (
                resolution is not None
                and int_num_clus_expected is not None
                and len(set(arr_cluster_label)) < int_num_clus_expected
            ):
                dict_kw_leiden_partition["resolution_parameter"] *= 1.2
                if self.verbose:
                    logger.info(
                        f"[Info] [RamData.leiden] resolution increased to {dict_kw_leiden_partition[ 'resolution_parameter' ]}"
                    )
            else:
                break
        del g

        """
        4) save labels
        """
        if (
            index_col_of_name_col_label is None
        ):  # assume 'name_col_label' is 1-dimensional column
            # update all columns
            ax.meta[name_col_label] = arr_cluster_label
        else:
            # update a single column in the meatadata column 'name_col_label'
            ax.meta[
                name_col_label, None, index_col_of_name_col_label
            ] = arr_cluster_label

        # report
        if self.verbose:
            logger.info(
                f"[Info] [RamData.leiden] clustering completed for {ax.meta.n_rows} number of barcodes"
            )

        # draw graphs
        if (
            name_col_embedding is not None
        ):  # visualize clustering results if 'name_col_embedding' has been given
            import seaborn as sns

            color_palette = sns.color_palette("Paired", len(set(arr_cluster_label)))
            cluster_colors = [
                color_palette[x] if x >= 0 else (0.5, 0.5, 0.5)
                for x in arr_cluster_label
            ]
            fig, plt_ax = plt.subplots(1, 1, figsize=(7, 7))
            plt_ax.scatter(
                *self.bc.meta[name_col_embedding, None, :2].T,
                c=cluster_colors,
                **dict_kw_scatter,
            )  # retrieve embedding data and draw the graph

        return

    """ for kNN-bsed label transfer """

    def train_label(
        self,
        name_model: str = "knn_classifier",
        n_neighbors: int = 10,
        name_col_label: str = "hdbscan",
        name_col_data: str = "X_pca",
        int_num_components_data: int = 20,
        axis: Union[int, str] = "barcodes",
        name_col_filter: str = "filter_label",
        dict_kw_pynndescent: dict = {
            "low_memory": True,
            "n_jobs": None,
            "compressed": False,
        },
        index_col_of_name_col_label: Union[int, None] = None,
    ) -> None:
        """# 2022-08-08 16:42:16
        build nearest-neighbor search index from the entries of the given axis, and using the labels of the entries, construct a kNN classifier

        arguments:
        === general ===
        'axis' : { 0 or 'barcodes' } for operating on the 'barcodes' axis, and { 1 or 'features' } for operating on the 'features' axis

        === nearest-neighbor search index ===
        'name_model' : name of the nearest-neighbor index and associated lables of the entries of the index that was saved/will be saved in the RamData.models database. if the model already exists, the index and the associated labels will be loadeded, and will be used to predict labels of the remaining entries.
        'n_neighbors' : the number of neighbors to use for the index
        'dict_kw_pynndescent' : the remaining arguments for constructing the index pynndescent.NNDescen 'model'

        === data input ===
        'name_col_filter' : the 'name_col' of the metadata of the given axis containing the filter marking the entries that will be used for trainining (building the index)
        'name_col_label' : the 'name_col' of the metadata of the given axis containing 'labels'.
        'index_col_of_name_col_label' : index of the secondary axis of the column of 'name_col_label' that will contain cluster labels. if None, 'name_col_label' is assumed to be a 1-dimensional column.
        'name_col_data' : the 'name_col' of the metadata of the given axis containing 'data' for building nearest-neighbor search.
        'int_num_components_data' : the number of components in the 'data' to use. for example, when 'int_num_components_data' is 2 and the 'data' contains 3 components, only the first two components will be used to build the index

        returns:
        labels, index
        """
        import pynndescent

        # handle inputs
        flag_axis_is_barcode = axis in {
            0,
            "barcode",
            "barcodes",
        }  # retrieve a flag indicating whether the data is summarized for each barcode or not

        ax = (
            self.bc if flag_axis_is_barcode else self.ft
        )  # retrieve the appropriate Axis object

        # set filters for operation
        if name_col_filter is not None:
            self.change_or_save_filter(name_col_filter)

        """
        2) Train model and retrieve cluster labels
        """
        # load the model and retrieve cluster labels
        type_model = "knn_classifier"
        model = self.load_model(name_model, type_model)
        if model is None:  # if the model does not exist, initiate the model
            # load training data
            data = ax.meta[name_col_data, None, :int_num_components_data]
            labels = (
                ax.meta[name_col_label]
                if index_col_of_name_col_label is None
                else ax.meta[name_col_label, None, index_col_of_name_col_label]
            )  # retrieve labels

            index = pynndescent.NNDescent(
                data, n_neighbors=n_neighbors, **dict_kw_pynndescent
            )
            index.prepare()  # prepare index for searching

            # save trained model
            if name_model is not None:  # check validity of 'name_model'
                self.save_model(
                    (labels, index), name_model, type_model
                )  # save model to the RamData # save both labels used for prediction and the index
        else:  # if the model with 'name_model' name exists in the database, use the previously saved model
            labels, index = model  # parse the model

        # report
        if self.verbose:
            logger.info(
                f"[Info] [RamData.train_label] training of labels completed for {ax.meta.n_rows} number of entries of the axis '{'barcodes' if flag_axis_is_barcode else 'features'}'"
            )

    def apply_label(
        self,
        name_model: str = "knn_classifier",
        name_col_label: str = "hdbscan",
        name_col_data: str = "X_pca",
        int_num_threads: int = 10,
        int_num_entries_in_a_batch: int = 10000,
        axis: Union[int, str] = "barcodes",
        name_col_filter: str = "filter_pca",
        index_col_of_name_col_label: Union[int, None] = None,
    ) -> dict:
        """# 2022-08-08 16:42:16
        using the previously constructed kNN classifier, predict labels of the entries by performing the nearest-neighbor search

        arguments:
        === general ===
        'axis' : { 0 or 'barcodes' } for operating on the 'barcodes' axis, and { 1 or 'features' } for operating on the 'features' axis
        'int_num_threads' : the number of threads to use for assigning labels. 3 ~ 10 are recommended.
        'int_num_entries_in_a_batch' : the number of entries to assign labels in each batch

        === nearest-neighbor search index ===
        'name_model' : name of the nearest-neighbor index and associated lables of the entries of the index that was saved/will be saved in the RamData.models database. if the model already exists, the index and the associated labels will be loadeded, and will be used to predict labels of the remaining entries.

        === data input ===
        'name_col_filter' : the name of 'feature'/'barcode' Axis metadata column to retrieve selection filter for running the current method. if None is given, current barcode/feature filters (if it has been set) will be used as-is.
        'name_col_label' : the 'name_col' of the metadata of the given axis that will contain assigned 'labels' (existing data will be overwritten).
        'index_col_of_name_col_label' : index of the secondary axis of the column of 'name_col_label' that will contain cluster labels. if None, 'name_col_label' is assumed to be a 1-dimensional column.
        'name_col_data' : the 'name_col' of the metadata of the given axis containing 'data' for building nearest-neighbor search index.
        'int_num_components_data' : the number of components in the 'data' to use. for example, when 'int_num_components_data' is 2 and the 'data' contains 3 components, only the first two components will be used to build the index

        returns:
        'dict_label_counter' : a dictionary containing counts of each unique label
        """
        """ prepare """
        # handle inputs
        flag_axis_is_barcode = axis in {
            0,
            "barcode",
            "barcodes",
        }  # retrieve a flag indicating whether the data is summarized for each barcode or not

        ax = (
            self.bc if flag_axis_is_barcode else self.ft
        )  # retrieve the appropriate Axis object

        # set filters for operation
        if name_col_filter is not None:
            self.change_filter(name_col_filter)

        """
        load model and the associated data objects
        """
        # load the model and retrieve cluster labels
        type_model = "knn_classifier"
        model = self.load_model(name_model, type_model)
        if model is None:  # if the model does not exist, initiate the model
            if self.verbose:
                logger.info(
                    f"[Error] [RamData.apply_label] the nearest-neighbor search index '{name_model}' does not exist, exiting"
                )
                return
        labels, index = model  # parse the model

        # retrieve the number of components for the model
        int_num_components_data = index.dim

        """
        assign labels
        """
        if self.verbose:
            logger.info(
                f"[Info] [RamData.apply_label] the nearest-neighbor search started"
            )
        # initialize the counter for counting labels
        dict_label_counter = dict()

        # define functions for multiprocessing step
        def process_batch(pipe_receiver_batch, pipe_sender_result):
            """# 2022-09-06 17:05:15"""
            while True:
                batch = pipe_receiver_batch.recv()
                if batch is None:
                    break
                # parse the received batch
                int_num_of_previously_returned_entries, l_int_entry_current_batch = (
                    batch["int_num_of_previously_returned_entries"],
                    batch["l_int_entry_current_batch"],
                )

                # retrieve data from the axis metadata
                data = ax.meta[
                    name_col_data, l_int_entry_current_batch, :int_num_components_data
                ]

                neighbors, distances = index.query(
                    data
                )  # retrieve neighbors using the index
                del data, distances

                labels_assigned = list(
                    bk.DICTIONARY_Find_keys_with_max_value(bk.COUNTER(labels[e]))[0][0]
                    for e in neighbors
                )  # assign labels using the labels of nearest neighbors
                del neighbors

                pipe_sender_result.send(
                    (l_int_entry_current_batch, labels_assigned)
                )  # send the result back to the main process

        pbar = progress_bar(
            desc="kNN search", total=ax.meta.n_rows
        )  # initialize the progress bar

        def post_process_batch(res):
            """# 2022-07-13 22:18:26"""
            # parse result
            l_int_entry_current_batch, labels_assigned = res
            int_num_retrieved_entries = len(l_int_entry_current_batch)

            # write the result to the axis metadata
            if (
                index_col_of_name_col_label is None
            ):  # assume 'name_col_label' is 1-dimensional column
                ax.meta[name_col_label, l_int_entry_current_batch] = labels_assigned
            else:  # update a single column in the meatadata column 'name_col_label'
                ax.meta[
                    name_col_label,
                    l_int_entry_current_batch,
                    index_col_of_name_col_label,
                ] = labels_assigned

            bk.COUNTER(
                labels_assigned, dict_counter=dict_label_counter
            )  # count assigned labels

            pbar.update(int_num_retrieved_entries)  # update the progress bar
            del labels_assigned

        # transform values using iPCA using multiple processes
        bk.Multiprocessing_Batch_Generator_and_Workers(
            ax.batch_generator(
                ax.filter,
                int_num_entries_for_batch=int_num_entries_in_a_batch,
                flag_mix_randomly=False,
            ),
            process_batch,
            post_process_batch=post_process_batch,
            int_num_threads=int_num_threads,
            int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
        )
        pbar.close()  # close the progress bar

        # return the counts of each unique label
        return dict_label_counter

    """ subsampling method """

    def subsample(
        self,
        name_model="leiden",
        int_num_entries_to_use: int = 30000,
        int_num_entries_to_subsample: int = 100000,
        int_num_iterations_for_subsampling: int = 2,
        name_col_data: str = "X_pca",
        int_num_components_data: int = 20,
        int_num_clus_expected: Union[int, None] = 20,
        name_col_label: str = "subsampling_label",
        name_col_avg_dist: str = "subsampling_avg_dist",
        axis: Union[int, str] = "barcodes",
        name_col_filter: str = "filter_pca",
        name_col_filter_subsampled: str = "filter_subsampled",
        resolution=0.7,
        directed: bool = True,
        use_weights: bool = True,
        dict_kw_leiden_partition: dict = {"n_iterations": -1, "seed": 0},
        dict_kw_pynndescent_transformer: dict = {
            "n_neighbors": 10,
            "metric": "euclidean",
            "low_memory": True,
        },
        n_neighbors: int = 20,
        dict_kw_pynndescent: dict = {
            "low_memory": True,
            "n_jobs": None,
            "compressed": False,
        },
        int_num_threads: int = 10,
        int_num_entries_in_a_batch: int = 10000,
    ):
        """# 2022-10-02 23:53:54
        subsample informative entries through iterative density-based subsampling combined with community detection algorithm

        arguments:
        === general ===
        'int_num_entries_to_use' : the number of entries to use during iterative subsampling
        'int_num_entries_to_subsample' : the number of entries to subsample
        'axis' : { 0 or 'barcodes' } for operating on the 'barcodes' axis, and { 1 or 'features' } for operating on the 'features' axis
        'int_num_threads' : the number of threads to use for nearest neighbor search. 3 ~ 10 are recommended.
        'int_num_entries_in_a_batch' : the number of entries in each batch for nearest neighbor search.

        === data input ===
        'name_col_filter' : the 'name_col' of the metadata of the given axis containing the filter marking the entries that will be used for trainining (building the index)
        'name_col_data' : the 'name_col' of the metadata of the given axis containing 'data' for building nearest-neighbor search index.
        'int_num_components_data' : the number of components in the 'data' to use. for example, when 'int_num_components_data' is 2 and the 'data' contains 3 components, only the first two components will be used to build the index

        === nearest-neighbor search index ===
        'n_neighbors' : the number of neighbors to use for the index
        'dict_kw_pynndescent' : the remaining arguments for constructing the index pynndescent.NNDescen 'model'

        === clustering arguments ===
        'resolution' : initial resolution of cluster. please refer to 'resolution_parameter' of 'leidenalg.find_partition' method
        'int_num_clus_expected' : the expected number of clusters in the data to optimize hyperparameters for community detection. if 'int_num_clus_expected' is not None, until the number of detected communities reaches 'int_num_clus_expected', the 'resolution' parameter will be optimized. this argument will be inactive when 'resolution' is None.
        'directed' : create directed graph. it is recommended to set it to True
        'use_weights' : use weights of the kNN graph for the leiden partitioning
        'dict_kw_leiden_partition' : a dictionary containing keyworded arguments for the 'leidenalg.find_partition' method
        'dict_kw_pynndescent_transformer' : a dictionary containing keyworded arguments for the 'pynndescent.PyNNDescentTransformer' method for constructing kNN graph from the data

        === iterative community-detection-and-density-based subsampling ===
        'name_model' : name of the kNN-clasifier model for predicting labels
        'int_num_iterations_for_subsampling' : the number of interations of subsampling operations

        === output ===
        'name_col_label' : the 'name_col' of the axis metadata that will contains clueter lables for each iteration.
        'name_col_avg_dist' : the 'name_col' of the axis metadata that will contains average distance of an entry to its nearest neighbors for each iteration.
        'name_col_filter_subsampled' : the 'name_col' of the metadata of the given axis containing the subsampled entries

        returns:
        """
        import pynndescent

        # handle inputs
        flag_axis_is_barcode = axis in {
            0,
            "barcode",
            "barcodes",
        }  # retrieve a flag indicating whether the data is summarized for each barcode or not

        ax = (
            self.bc if flag_axis_is_barcode else self.ft
        )  # retrieve the appropriate Axis object

        # initialize output columns in the metadata
        ax.meta.initialize_column(
            name_col_label,
            dtype=np.int32,
            shape_not_primary_axis=(int_num_iterations_for_subsampling,),
            chunks=(1,),
            categorical_values=None,
        )
        ax.meta.initialize_column(
            name_col_avg_dist,
            dtype=np.float64,
            shape_not_primary_axis=(int_num_iterations_for_subsampling,),
            chunks=(1,),
            categorical_values=None,
        )

        # set filters for operation
        if name_col_filter is None:
            if self.verbose:
                logger.info(
                    f"[Error] [RamData.subsample] 'name_col_filter' should not be None, exiting"
                )
            return
        self.change_or_save_filter(name_col_filter)

        # when the number of entries is below 'int_num_entries_to_subsample'
        if int_num_entries_to_subsample >= ax.meta.n_rows:
            """if no subsampling is required, save the current filter as the subsampled filter, and exit"""
            self.save_filter(name_col_filter_subsampled)
            return

        # perform initial random sampling
        ax.filter = ax.subsample(
            min(1, int_num_entries_to_use / ax.meta.n_rows)
        )  # retrieve subsampling ratio
        self.save_filter(name_col_filter_subsampled)  # save subsampled filter

        type_model = "knn_classifier"
        for index_iteration in range(
            int_num_iterations_for_subsampling
        ):  # for each iteration
            if self.verbose:
                logger.info(
                    f"[Info] [RamData.subsample] iteration #{index_iteration} started."
                )
            """
            community detection - leiden
            """
            # perform leiden clustering
            self.leiden(
                name_model=None,
                name_col_data=name_col_data,
                int_num_components_data=int_num_components_data,
                name_col_label=name_col_label,
                resolution=resolution,
                int_num_clus_expected=int_num_clus_expected,
                directed=directed,
                use_weights=use_weights,
                dict_kw_leiden_partition=dict_kw_leiden_partition,
                dict_kw_pynndescent_transformer=dict_kw_pynndescent_transformer,
                name_col_filter=None,
                name_col_embedding=None,
                index_col_of_name_col_label=index_iteration,
            )  # clustering result will be saved 'index_iteration' column in the 'name_col_label' # does not save model

            # assign labels and retrieve label counts
            self.delete_model(name_model, type_model)  # reset the model before training
            self.train_label(
                name_model=name_model,
                n_neighbors=n_neighbors,
                name_col_label=name_col_label,
                name_col_data=name_col_data,
                int_num_components_data=int_num_components_data,
                axis=axis,
                name_col_filter=None,
                dict_kw_pynndescent=dict_kw_pynndescent,
                index_col_of_name_col_label=index_iteration,
            )
            dict_label_count = self.apply_label(
                name_model=name_model,
                name_col_label=name_col_label,
                name_col_data=name_col_data,
                int_num_threads=int_num_threads,
                int_num_entries_in_a_batch=int_num_entries_in_a_batch,
                axis=axis,
                name_col_filter=name_col_filter,
                index_col_of_name_col_label=index_iteration,
            )  # assign labels to 'name_col_filter' entries

            """
            calculate density - build knn search index
            """
            if self.verbose:
                logger.info(
                    f"[Info] [RamData.subsample] iteration #{index_iteration} calculating density information started"
                )

            # prepare knn search index
            self.change_filter(
                name_col_filter_subsampled
            )  # change filter to currently subsampled entries for building knn search index
            index = pynndescent.NNDescent(
                ax.meta[name_col_data, None, :int_num_components_data],
                n_neighbors=n_neighbors,
                **dict_kw_pynndescent,
            )
            index.prepare()  # prepare index for searching

            """
            calculate density - summarize the distances
            """
            self.change_filter(
                name_col_filter
            )  # change filter to all the query entries for estimating density
            dict_label_total_avg_dist = (
                dict()
            )  # initialize the dictionary for surveying the the total 'average distance' values of the entries belonging to each unique label

            # define functions for multiprocessing step
            def process_batch(pipe_receiver_batch, pipe_sender_result):
                """# 2022-09-06 17:10:30"""
                while True:
                    batch = pipe_receiver_batch.recv()
                    if batch is None:
                        break
                    # parse the received batch
                    (
                        int_num_of_previously_returned_entries,
                        l_int_entry_current_batch,
                    ) = (
                        batch["int_num_of_previously_returned_entries"],
                        batch["l_int_entry_current_batch"],
                    )

                    # retrieve data from the axis metadata
                    data = ax.meta[
                        name_col_data,
                        l_int_entry_current_batch,
                        :int_num_components_data,
                    ]

                    neighbors, distances = index.query(
                        data
                    )  # retrieve neighbors using the index
                    del data, neighbors

                    pipe_sender_result.send(
                        (l_int_entry_current_batch, distances.mean(axis=1))
                    )  # calculate average distances of the entries in a batch # send the result back to the main process

            pbar = progress_bar(
                desc="collecting density information", total=ax.meta.n_rows
            )  # initialize the progress bar

            def post_process_batch(res):
                """# 2022-07-13 22:18:26"""
                # parse result
                l_int_entry_current_batch, arr_avg_dist = res
                int_num_retrieved_entries = len(l_int_entry_current_batch)

                # write the result to the axis metadata
                ax.meta[
                    name_col_avg_dist, l_int_entry_current_batch, index_iteration
                ] = arr_avg_dist

                # retrieve assigned labels, and summarize calculated average distances
                for label, avg_dist in zip(
                    ax.meta[name_col_label, l_int_entry_current_batch, index_iteration],
                    arr_avg_dist,
                ):
                    if label not in dict_label_total_avg_dist:
                        dict_label_total_avg_dist[label] = 0
                    dict_label_total_avg_dist[
                        label
                    ] += avg_dist  # update total avg_dist of the label

                pbar.update(int_num_retrieved_entries)  # update the progress bar

            # transform values using iPCA using multiple processes
            bk.Multiprocessing_Batch_Generator_and_Workers(
                ax.batch_generator(
                    ax.filter,
                    int_num_entries_for_batch=int_num_entries_in_a_batch,
                    flag_mix_randomly=False,
                ),
                process_batch,
                post_process_batch=post_process_batch,
                int_num_threads=int_num_threads,
                int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
            )
            pbar.close()  # close the progress bar

            """
            using the summarized metrics, prepare subsampling
            """
            # calculate the number of entries to subsample for each unique label
            int_num_labels = max(dict_label_count) + 1  # retrieve the number of labels

            # convert type of 'dict_label_count' to numpy ndarray # leiden labels are 0-based coordinate-based
            arr_label_count = np.zeros(int_num_labels)
            for label in dict_label_count:
                arr_label_count[label] = dict_label_count[label]

            int_num_entries_to_include = (
                int_num_entries_to_subsample
                if index_iteration == int_num_iterations_for_subsampling - 1
                else int_num_entries_to_use
            )  # if the current round is the last round, include 'int_num_entries_to_subsample' number of entries in the output filter. if not, include 'int_num_entries_to_use' number of entries for next iteration

            int_label_count_current_threshold = int(
                int_num_entries_to_include / int_num_labels
            )  # initialize the threshold
            for index_current_label in np.argsort(
                arr_label_count
            ):  # from label with the smallest number of entries to label with the largest number of entries
                int_label_count = arr_label_count[index_current_label]
                if int_label_count > int_label_count_current_threshold:
                    break
                # reset 'int_label_count_current_threshold' using the remaining number of entries and labels
                arr = arr_label_count[arr_label_count <= int_label_count]
                int_label_count_current_threshold = int(
                    (int_num_entries_to_include - arr.sum())
                    / (int_num_labels - len(arr))
                )

            # retrieve number of entries to subsample for each label
            arr_label_count_subsampled = deepcopy(arr_label_count)
            arr_label_count_subsampled[
                arr_label_count_subsampled > int_label_count_current_threshold
            ] = int_label_count_current_threshold

            # compose name space for subsampling
            dict_ns = dict(
                (
                    label,
                    {
                        "int_num_entries_remaining_to_reject": dict_label_count[label]
                        - arr_label_count_subsampled[label],
                        "int_num_entries_remaining_to_accept": arr_label_count_subsampled[
                            label
                        ],
                    },
                )
                for label in dict_label_count
            )

            if self.verbose:
                logger.info(
                    f"[Info] [RamData.subsample] iteration #{index_iteration} subsampling started"
                )

            # define functions for multiprocessing step
            def process_batch(pipe_receiver_batch, pipe_sender_result):
                """# 2022-09-06 17:10:30"""
                while True:
                    batch = pipe_receiver_batch.recv()
                    if batch is None:
                        break
                    # parse the received batch
                    (
                        int_num_of_previously_returned_entries,
                        l_int_entry_current_batch,
                    ) = (
                        batch["int_num_of_previously_returned_entries"],
                        batch["l_int_entry_current_batch"],
                    )

                    pipe_sender_result.send(
                        (
                            l_int_entry_current_batch,
                            ax.meta[
                                name_col_label,
                                l_int_entry_current_batch,
                                index_iteration,
                            ],
                            ax.meta[
                                name_col_avg_dist,
                                l_int_entry_current_batch,
                                index_iteration,
                            ],
                        )
                    )  # retrieve data from the axis metadata and # send result back to the main process

            pbar = progress_bar(
                desc=f"subsampling", total=ax.meta.n_rows
            )  # initialize the progress bar

            def post_process_batch(res):
                """# 2022-07-13 22:18:26
                perform PCA transformation for each batch
                """
                # parse result
                l_int_entry_current_batch, arr_labels, arr_avg_dist = res
                int_num_retrieved_entries = len(l_int_entry_current_batch)

                # initialize selection result
                arr_selection = np.zeros(
                    len(arr_labels), dtype=bool
                )  # no selected entries by default

                for index in range(
                    len(arr_labels)
                ):  # iterate through each entry by entry
                    label, avg_dist = (
                        arr_labels[index],
                        arr_avg_dist[index],
                    )  # retrieve data of an entry

                    # if no entry should be rejected, select
                    if dict_ns[label]["int_num_entries_remaining_to_reject"] == 0:
                        arr_selection[index] = True
                        dict_ns[label][
                            "int_num_entries_remaining_to_accept"
                        ] -= 1  # update 'int_num_entries_remaining_to_accept'
                    else:
                        if (
                            (
                                dict_ns[label]["int_num_entries_remaining_to_accept"]
                                / dict_ns[label]["int_num_entries_remaining_to_reject"]
                            )
                            * avg_dist
                            / dict_label_total_avg_dist[label]
                        ) > np.random.random():  # determine whether the current entry should be included in the subsampled result
                            arr_selection[index] = True
                            dict_ns[label][
                                "int_num_entries_remaining_to_accept"
                            ] -= 1  # update 'int_num_entries_remaining_to_accept'
                        else:
                            dict_ns[label][
                                "int_num_entries_remaining_to_reject"
                            ] -= 1  # update 'int_num_entries_remaining_to_reject'

                # write the subsampled result to the axis metadata
                ax.meta[
                    name_col_filter_subsampled, l_int_entry_current_batch
                ] = arr_selection

                pbar.update(int_num_retrieved_entries)  # update the progress bar

            # transform values using iPCA using multiple processes
            bk.Multiprocessing_Batch_Generator_and_Workers(
                ax.batch_generator(
                    ax.filter,
                    int_num_entries_for_batch=int_num_entries_in_a_batch,
                    flag_mix_randomly=False,
                ),
                process_batch,
                post_process_batch=post_process_batch,
                int_num_threads=min(3, int_num_threads),
                int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
            )
            pbar.close()  # close the progress bar

            # prepare next batch
            self.change_filter(
                name_col_filter_subsampled
            )  # change filter to currently subsampled entries for the next round

    def subsample_for_each_clus(
        self,
        name_col_label: str,
        int_num_entries_to_subsample: int = 100000,
        index_col_of_name_col_label: Union[int, None] = -1,
        name_col_filter: str = "filter_pca",
        name_col_filter_subsampled: Union[str, None] = None,
    ):
        """# 2022-11-15 02:13:41

        perform simple subsampling by selecting a fixed number of cells for each cluster

        int_num_entries_to_subsample : int = 100000 # the number of entries to subsample
        name_col_label : str # the name of column of the 'barcode' axis containing cluster labels
        index_col_of_name_col_label : Union[ int, None ] = -1 # index of the column containing cluster labels
        name_col_filter : str = 'filter_pca' # the name of the input column of the 'barcode' axis containing the input barcode filter
        name_col_filter_subsampled : Union[ str, None ] = None # the name of the output column of the 'barcode' axis containing the output, a subsampled barcode filter
        """
        # retrieve axis
        ax = self.bc

        if name_col_label not in ax.meta:
            if self.verbose:
                logger.info(
                    f"[Error] [RamData.subsample_for_each_clus] name_col_label '{name_col_label}' does not exist, exiting"
                )
            return

        # set filters for operation
        ax.change_or_save_filter(name_col_filter)

        # retrieve labels
        arr_label = (
            ax.meta[name_col_label]
            if len(ax.meta.get_zarr(name_col_label).shape) == 1
            else ax.meta[name_col_label, None, index_col_of_name_col_label]
        )  # check whether the dimension of the column containing labels is 1D or 2D

        s_count_label = bk.LIST_COUNT(arr_label, duplicate_filter=False)
        s_count_label.sort_values(inplace=True)  # sort by cluster size

        """
        retrieve the number of entries to subsample for each cluster
        """
        dict_name_clus_to_num_entries_to_be_subsampled = dict()
        int_num_entries_to_subsample_remaining = int_num_entries_to_subsample
        int_num_clus_remaining = len(s_count_label)
        for name_clus, size_clus in zip(
            s_count_label.index.values, s_count_label.values
        ):  # iterate clusters (from smallest cluster to largest cluster)
            # retrieve the number of entries to be subsampled for each cluster
            int_max_num_entries_for_each_clus = math.floor(
                int_num_entries_to_subsample_remaining / int_num_clus_remaining
            )
            int_num_entries_to_be_subsampled_for_a_clus = (
                size_clus
                if size_clus <= int_max_num_entries_for_each_clus
                else int_max_num_entries_for_each_clus
            )

            # retrieve the number of subsampled entries for each cluster
            dict_name_clus_to_num_entries_to_be_subsampled[
                name_clus
            ] = int_num_entries_to_be_subsampled_for_a_clus

            # update tne number of entries and clusters
            int_num_entries_to_subsample_remaining -= (
                int_num_entries_to_be_subsampled_for_a_clus
            )
            int_num_clus_remaining -= 1

        # retrieve the number of entries for each cluster
        dict_name_clus_to_num_entries_remaining = s_count_label.to_dict()
        dict_name_clus_to_num_entries_to_be_subsampled_remaining = (
            dict_name_clus_to_num_entries_to_be_subsampled
        )

        # initialize a new bitarray that will contain subsampled entries
        ba_subsampled = bitarray(ax.int_num_entries)
        ba_subsampled.setall(0)
        # iterate over label and int_entry
        for label, int_entry in zip(arr_label, BA.find(ax.filter)):
            if (
                np.random.random()
                < dict_name_clus_to_num_entries_to_be_subsampled_remaining[label]
                / dict_name_clus_to_num_entries_remaining[label]
            ):  # determine whether to subsample an entry
                ba_subsampled[int_entry] = 1  # select the entry
                dict_name_clus_to_num_entries_to_be_subsampled_remaining[
                    label
                ] -= 1  # consume 'dict_name_clus_to_num_entries_to_be_subsampled_remaining'
            dict_name_clus_to_num_entries_remaining[
                label
            ] -= 1  # consume 'dict_name_clus_to_num_entries_remaining'

        # apply subsampling
        ax.filter = ba_subsampled

        # if valid 'name_col_filter_subsampled' has been given, save the filter containing subsampled barcodes as the column of the name 'name_col_filter_subsampled'
        if name_col_filter_subsampled is not None:
            ax.save_filter(name_col_filter_subsampled)

    """ scanpy api wrappers """

    def run_scanpy_using_pca(
        self,
        name_col_pca: str = "X_pca",
        int_num_pca_components: int = 30,
        int_neighbors_n_neighbors: int = 10,
        int_neighbors_n_pcs: int = 30,
        set_method: set = {"leiden", "umap"},
        path_file_adata: Union[None, str] = None,
        str_suffix: str = "_scanpy",
        dict_kw_neighbors: dict = dict(),
        dict_kw_umap: Union[Dict, List[Dict]] = dict(),
        dict_kw_leiden: Union[Dict, List[Dict]] = dict(),
        dict_kw_tsne: Union[Dict, List[Dict]] = dict(),
        int_num_processes: int = 5,
    ):
        """# 2022-12-29 04:43:45
        run scanpy methods using the PCA values calculated using scelephant

        name_col_pca : str = 'X_pca' #
        int_num_pca_components : int = 30 # the number of PCA components to retrieve from RamData
        int_neighbors_n_neighbors : int = 10 # the number of neighbors to include in the neighborhood graph
        int_neighbors_n_pcs : int = 30 # the number of PCA components for building the neighborhood graph
        set_method = { 'leiden', 'umap' } # scanpy methods to use
        str_suffix = '_scanpy' # suffix for the output column names of the 'barcodes' metadata
        path_file_adata : Union[ None, str ] = None # if a non-None value is given, write AnnData object containing connectivities (adjacency matrix) to the given path. if '.h5ad' suffix is not present, the suffix will be added.
        dict_kw_neighbors = dict( ) # keyworded arguments for scanpy umap method
        dict_kw_umap : Union[ Dict, List[ Dict ] ] = dict( ) # a dictionary containing keyworded arguments for scanpy umap method*.
        dict_kw_tsne : Union[ Dict, List[ Dict ] ] = dict( ) # a dictionary containing keyworded arguments for scanpy tsne method*.
        dict_kw_leiden : Union[ Dict, List[ Dict ] ] = dict( ) # a dictionary containing keyworded arguments for scanpy leiden method*.
            *when a list of dictionaries are given, analysis will be performed multiple times. If a list of dictionaries are given, each dictionary should include 'str_suffix_run' for adding run-specific suffix to the output column

        int_num_processes : int = 5 # the number of processes for running leiden clustering process in parallel. actual number of processes that will perform the leiden clustering will be 'int_num_processes' - 2, considering processes for generating work load and post-processing of the output (for more information, please refer to biobookshelf.main.Multiprocessing_Batch_Generator_and_Workers)
        """
        import scanpy as sc

        # if no set_method was given, exit early
        if len(set_method) == 0:
            return

        # process 'path_file_adata' input
        if path_file_adata is not None:
            path_file_adata = (
                path_file_adata
                if path_file_adata[-5:].lower() == ".h5ad"
                else f"{path_file_adata}.h5ad"
            )  # add '.h5ad' suffix if the suffix is not present

        # attemps to read adjacency matrix from an existing file (if given)
        flag_adata_loaded = False  # initialize the flag
        if path_file_adata is not None and filesystem_operations(
            "exists", path_file_adata
        ):  # if a path to the given anndata was given appears to be not empty
            try:  # attemps to read the adjacency matrix
                adata = sc.read_h5ad(path_file_adata)
                flag_adata_loaded = True  # the flag
                if self.verbose:
                    logger.info(
                        f"[RamData.run_scanpy_using_pca] AnnData was loaded from {path_file_adata}"
                    )
            except:
                pass
        # fetch PCA values from RamData and calculate adjacency matrix
        if (
            not flag_adata_loaded
        ):  # if adjacency matrix is not available, calculate adjacency matrix
            # retrieve anndata and calculate the neighborhood graph
            adata = self[
                :, [{name_col_pca}], [], []
            ]  # load all barcodes in the filter, no feature in the filter, load PCA data only, load no feature metadata
            if self.verbose:
                logger.info("[RamData.run_scanpy_using_pca] anndata retrieved.")

            # build a neighborhood graph
            sc.pp.neighbors(
                adata,
                n_neighbors=int_neighbors_n_neighbors,
                n_pcs=int_neighbors_n_pcs,
                use_rep=name_col_pca,
                **dict_kw_neighbors,
            )
            if self.verbose:
                logger.info(
                    "[RamData.run_scanpy_using_pca] K-nearest neighbor graphs calculation completed."
                )
            if (
                path_file_adata is not None
            ):  # if a valid value has been given for 'path_file_adata'
                adata.write(path_file_adata)
                if self.verbose:
                    logger.info(
                        f"[RamData.run_scanpy_using_pca] AnnData containing the calculated adjacency matrix has been saved to {path_file_adata}"
                    )
        # perform analysis
        if "umap" in set_method:
            if isinstance(
                dict_kw_umap, dict
            ):  # wrap a single dictionary with a list the
                dict_kw_umap = [dict_kw_umap]
            for dict_kw in dict_kw_umap:
                str_suffix_run = dict_kw.pop(
                    "str_suffix_run", ""
                )  # retrieve 'str_suffix_run' (default is '')
                name_col = (
                    f"X_umap{str_suffix}{str_suffix_run}"  # compose the column name
                )
                sc.tl.umap(adata, **dict_kw)  # perform analysis using scanpy
                self.bc.meta[name_col] = adata.obsm["X_umap"]  # save result to RamData
                if self.verbose:
                    logger.info(
                        f"[RamData.run_scanpy_using_pca] UMAP calculation completed, and the resulting UMAP-embedding was saved to the '{name_col}' column of the RamData."
                    )
        # perform analysis
        if "tsne" in set_method:
            if isinstance(
                dict_kw_tsne, dict
            ):  # wrap a single dictionary with a list the
                dict_kw_tsne = [dict_kw_tsne]
            for dict_kw in dict_kw_tsne:
                str_suffix_run = dict_kw.pop(
                    "str_suffix_run", ""
                )  # retrieve 'str_suffix_run' (default is '')
                sc.tl.tsne(
                    adata, use_rep=name_col_pca, **dict_kw
                )  # perform analysis using scanpy
                name_col = (
                    f"X_tsne{str_suffix}{str_suffix_run}"  # compose the column name
                )
                self.bc.meta[name_col] = adata.obsm["X_tsne"]  # save result to RamData
                if self.verbose:
                    logger.info(
                        f"[RamData.run_scanpy_using_pca] calculation of tSNE embedding completed, and the resulting embedding was saved to the '{name_col}' column of the RamData."
                    )
        if "leiden" in set_method:
            if isinstance(
                dict_kw_leiden, dict
            ):  # wrap a single dictionary with a list the
                dict_kw_leiden = [dict_kw_leiden]
            if (
                len(dict_kw_leiden) == 1 or int_num_processes <= 3
            ):  # using a leiden clustering in the main process only.
                for dict_kw in dict_kw_leiden:  # for each 'dict_kw'
                    str_suffix_run = dict_kw.pop(
                        "str_suffix_run", ""
                    )  # retrieve 'str_suffix_run' (default is '')
                    name_col = (
                        f"leiden{str_suffix}{str_suffix_run}"  # compose the column name
                    )
                    sc.tl.leiden(
                        adata, key_added=name_col, **dict_kw
                    )  # perform leiden clustering
                    self.bc.meta[name_col] = adata.obs[
                        name_col
                    ]  # save result to RamData
                    if self.verbose:
                        logger.info(
                            f"[RamData.run_scanpy_using_pca] leiden clustering completed, and the resulting cluster membership information was saved to the '{name_col}' column of the RamData."
                        )
            else:  # when multiple clustering runs should be run
                import joblib  # for persistent, reference-counting-free memory

                # save the adjacency matrix for persistent access
                path_file_X = f"{self.path_folder_temp}{bk.UUID( )}.pickle"
                joblib.dump(
                    adata.obsp["connectivities"], path_file_X
                )  # dump the sparse matrix for paralleled access

                # delete the adjacency matrix from the input AnnData object to avoid a redundant data copying
                del adata.obsp["distances"]
                del adata.obsp["connectivities"]

                X = joblib.load(path_file_X)  # load the sparse matrix
                ram = self  # retrieve the reference to the self

                def __run_leiden(pipe_receiver, pipe_sender):
                    """# 2022-12-24 03:10:58"""
                    ram_fork_safe = (
                        ram.get_fork_safe_version()
                    )  # retrieve a fork-safe version of the RamData (for file-locking)
                    while True:
                        ins = pipe_receiver.recv()
                        if ins is None:
                            break
                        dict_kw = ins  # parse input

                        str_suffix_run = dict_kw.pop(
                            "str_suffix_run", ""
                        )  # retrieve 'str_suffix_run' (default is '')
                        name_col = f"leiden{str_suffix}{str_suffix_run}"  # compose the column name

                        sc.tl.leiden(
                            adata, adjacency=X, key_added=name_col, **dict_kw
                        )  # perform leiden clustering
                        ram_fork_safe.bc.meta[name_col] = (
                            adata.obs[name_col].values.astype(str).astype(object)
                        )  # save result to the current RamData # convert integer values to string values

                        if self.verbose:
                            logger.info(
                                f"[RamData.run_scanpy_using_pca] leiden clustering completed, and the resulting cluster membership information was saved to the '{name_col}' column of the RamData."
                            )

                        pipe_sender.send(
                            "completed"
                        )  # report the completion of the work
                    self.terminate_spawned_processes()  # terminate the spawned processes

                # run works using multiple workers
                bk.Multiprocessing_Batch_Generator_and_Workers(
                    gen_batch=iter(dict_kw_leiden),
                    process_batch=__run_leiden,
                    int_num_threads=int_num_processes,
                )
                filesystem_operations("rm", path_file_X)  # delete the temporary file
        return adata  # return the resulting anndata

    """ knn-index based embedding/classification """

    def train_knn(
        self,
        name_model: str,
        name_col_x: str,
        name_col_filter_training: Union[str, None] = None,
        axis: Union[int, str] = "barcodes",
        int_num_components_x: Union[None, int] = None,
        n_neighbors: int = 10,
        int_num_entries_in_a_batch: int = 10000,
        int_num_threads: int = 10,
        dict_kw_pynndescent: dict = {
            "low_memory": True,
            "n_jobs": None,
            "compressed": False,
        },
        name_col_filter_for_collecting_neighbors: Union[None, str] = None,
        int_num_nearest_neighbors_to_collect: int = 3,
    ):
        """# 2023-01-02 09:40:06

        use knn index built from subsampled entries to classify (predict labels) or embed (predict embeddings) barcodes.

        name_model : str # the name of the output model containing knn index
        name_col_x : str # the name of the column containing X (input) data
        name_col_filter_training : str # the name of the column containing filter for entries that will be used for training
        axis : Union[ int, str ] = 'barcodes' # axis from which to retrieve X
        int_num_components_x : Union[ None, int ] = None # by default, use all components available in X
        n_neighbors : int = 10 # the number of neighbors to use
        dict_kw_pynndescent : dict = { 'low_memory' : True, 'n_jobs' : None, 'compressed' : False } # the additional keyworded arguments for pynndescent index

        === for recording neighbors of the entries of the index ===
        name_col_filter_for_collecting_neighbors : Union[ None, str ] = None # the name of the column containing filter for entries that will be queried against the built knnindex to identify neighbors of the entries that were used to build the index
        int_num_nearest_neighbors_to_collect : int = 3 # the number of nearest neighbors to collect
        int_num_entries_in_a_batch : int = 10000 # the number of entries in a batch for each process. the larger the batch size is, the larger memory each process consumes.
        """
        import pynndescent

        # handle inputs
        flag_axis_is_barcode = self._determine_axis(
            axis
        )  # retrieve a flag indicating whether the data is summarized for each barcode or not

        ax = (
            self.bc if flag_axis_is_barcode else self.ft
        )  # retrieve the appropriate Axis object

        # set filters for operation
        if name_col_filter_training is not None:
            ax.change_or_save_filter(name_col_filter_training)

        # retrieve flags
        flag_collect_neighbors = (
            name_col_filter_for_collecting_neighbors in ax.columns
            and int_num_nearest_neighbors_to_collect > 0
            and not ax.are_all_entries_active
        )  # in order to collect neighbors, knnindex should only contains a subset of entries in the axis

        # exit if the input column does not exist
        if name_col_x not in ax.meta:
            logger.error(f"[train_knn] {name_col_x} column does not exist")
            return

        """
        2) Train model and retrieve cluster labels
        """
        # load the model and retrieve cluster labels
        type_model = "knnindex"
        if self.check_model(name_model, type_model):  # if the model exists, exit early
            if self.verbose:
                logging.info(f"the output model '{name_model}' already exists, exiting")
            return

        if (
            len(self.bc.meta.get_shape(name_col_x)) == 0 or int_num_components_x is None
        ):  # if only a single component is available or 'int_num_components_x' is None, use all components
            int_num_components_x = None  # correct 'int_num_components_x' if only single component is available but
            X = ax.meta[
                name_col_x,
                None,
            ]  # load all components
        else:
            X = ax.meta[
                name_col_x, None, :int_num_components_x
            ]  # load top 'int_num_components_x' number of components
        if self.verbose:
            logging.info(f"data for building the knnindex '{name_model}' was retrieved")

        knnindex = pynndescent.NNDescent(
            X, n_neighbors=n_neighbors, **dict_kw_pynndescent
        )
        knnindex.prepare()  # prepare index for searching
        if self.verbose:
            logging.info(f"the knnindex '{name_model}' was built")
        """
        assign labels or retrieve embeddings
        """
        ba_filter_knnindex = ax.filter  # retrieve a filter of entries of the knnindex
        int_num_entries_in_the_knnindex = (
            ba_filter_knnindex.count()
        )  # retrieve the number of entries in the knnindex
        arr_neighbors, arr_neighbors_index = None, None
        if flag_collect_neighbors:
            if self.verbose:
                logging.info(f"[RamData.train_knn] the nearest-neighbor search started")

            # set appropriate filter
            ax.change_filter(name_col_filter_for_collecting_neighbors)
            ax.exclude(
                ba_filter_knnindex
            )  # exclude entries used in the knnindex during kNN search

            # define a namespace
            ns = dict()
            ns["l_neighbors"] = [[] for i in range(int_num_entries_in_the_knnindex)]

            # define functions for multiprocessing step
            def process_batch(pipe_receiver_batch, pipe_sender_result):
                """# 2022-09-06 17:05:15"""
                while True:
                    batch = pipe_receiver_batch.recv()
                    if batch is None:
                        break
                    # parse the received batch
                    (
                        int_num_of_previously_returned_entries,
                        l_int_entry_current_batch,
                    ) = (
                        batch["int_num_of_previously_returned_entries"],
                        batch["l_int_entry_current_batch"],
                    )

                    # retrieve data from the axis metadata
                    X = ax.meta[
                        name_col_x, l_int_entry_current_batch, :int_num_components_x
                    ]

                    neighbors, distances = knnindex.query(
                        X
                    )  # retrieve neighbors using the index
                    del X, distances

                    # use only 'int_num_nearest_neighbors' number of nearest neighbors
                    if int_num_nearest_neighbors_to_collect < knnindex.n_neighbors:
                        neighbors = neighbors[:, :int_num_nearest_neighbors_to_collect]

                    pipe_sender_result.send(
                        (l_int_entry_current_batch, neighbors)
                    )  # send the result back to the main process

            logger.info(
                f"Searching neighbors of the {int_num_entries_in_the_knnindex} entries in the index"
            )
            pbar = progress_bar(
                desc=f"neighbors of {int_num_entries_in_the_knnindex} entries",
                total=ax.meta.n_rows,
            )  # initialize the progress bar

            def post_process_batch(res):
                """# 2022-07-13 22:18:26"""
                # parse result
                l_int_entry_current_batch, neighbors = res
                int_num_retrieved_entries = len(l_int_entry_current_batch)

                for int_entry, neighbors_of_an_entry in zip(
                    l_int_entry_current_batch, neighbors
                ):
                    for i in neighbors_of_an_entry:
                        ns["l_neighbors"][i].append(int_entry)
                del neighbors

                pbar.update(int_num_retrieved_entries)  # update the progress bar

            # transform values using iPCA using multiple processes
            bk.Multiprocessing_Batch_Generator_and_Workers(
                ax.batch_generator(
                    ax.filter,
                    int_num_entries_for_batch=int_num_entries_in_a_batch,
                    flag_mix_randomly=False,
                ),
                process_batch,
                post_process_batch=post_process_batch,
                int_num_threads=int_num_threads,
                int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
            )
            pbar.close()  # close the progress bar

            # build 'arr_neighbors' and 'arr_neighbors_index'
            l_neighbors = ns["l_neighbors"]
            int_pos = 0
            l, l_index = [], [0]
            for neighbors in l_neighbors:
                l.extend(neighbors)
                int_pos += len(neighbors)
                l_index.append(int_pos)
            del l_neighbors
            arr_neighbors, arr_neighbors_index = np.array(l), np.array(l_index)
            del l, l_index

            # reset the axis filter
            ax.filter = ba_filter_knnindex

        # save trained model
        model = {
            "flag_axis_is_barcode": flag_axis_is_barcode,
            "dict_kw_pynndescent": dict_kw_pynndescent,
            "int_num_nearest_neighbors_to_collect": int_num_nearest_neighbors_to_collect,
            "name_col_filter_for_collecting_neighbors": name_col_filter_for_collecting_neighbors,
            "name_col_x": name_col_x,
            "int_num_components_x": int_num_components_x,
            "int_num_entries_in_the_knnindex": int_num_entries_in_the_knnindex,
            "filter": ba_filter_knnindex,
            "identifier": self.identifier,
            "knnindex": knnindex,
            "arr_neighbors": arr_neighbors,
            "arr_neighbors_index": arr_neighbors_index,
        }
        self.save_model(
            model, name_model, type_model
        )  # save model to the RamData # save filter along with index (compressed filter for 20M entries is ~ 3MB) # save identifer of the current RamData, too

        # report
        if self.verbose:
            logger.info(
                f"[RamData.train_knn] knn index building completed for {ax.meta.n_rows} number of entries of the axis '{'barcodes' if flag_axis_is_barcode else 'features'}' using the data from the column '{name_col_x}'"
            )

    def apply_knn(
        self,
        name_model: str,
        name_col_y_input: str,
        name_col_y_output: Union[str, None] = None,
        name_col_x: Union[str, None] = None,
        name_col_filter_query: Union[str, None] = None,
        name_col_filter_neighbors_of_the_query: Union[str, None] = None,
        flag_include_secondary_neighbors_of_the_query: bool = True,
        int_num_nearest_neighbors: Union[int, None] = None,
        operation: Literal["classifier", "embedder"] = "embedder",
        float_std_ratio_for_outlier_detection: float = 0.1,
        axis: Union[None, int, str] = None,
        linkage_for_agglomerative_clustering_of_embeddings_of_neighbors: Literal[
            "single", "complete", "ward", "average"
        ] = "complete",
        flag_use_agglomerative_clustering_of_embeddings_of_neighbors_for_outlier_detection: bool = True,
        int_num_entries_in_a_batch: int = 10000,
        int_num_threads: int = 10,
        int_index_component_reference: Union[None, int] = None,
    ):
        """# 2022-12-21 00:43:32

        use knn index built from subsampled entries to classify (predict labels) or embed (predict embeddings) barcodes.

        name_model : str # the name of the model containing knn index
        name_col_x : str # the name of the column containing X (input) data. by default (if None is given), name_col_x stored in the model will be used.
        name_col_y_input : str # the name of the column containing y (input) data.
        name_col_y_output : Union[ str, None ] = None # the name of the column containing y (output) data. by default (if None is given), output will be written to 'name_col_y_input', which will overwrite existing data
        name_col_filter_query : Union[ str, None ] = None # the name of column containing filter for query entries to which the model will be applied. if None is given, all currently active entries will be queried.
        name_col_filter_neighbors_of_the_query : Union[ str, None ] = None # the name of output filter column where neighbor entries of the queried entries were marked 'True'.
        flag_include_secondary_neighbors_of_the_query : bool = True # a flag indicating whether to collect neighbors of the entries used to build the knnindex
        int_num_nearest_neighbors : Union[ int, None ] = None # the number of nearest neighbors to use (should be equal or smaller than the number of neighbors of the index). By default, all neighbors returned by a kNN index will be used.
        operation : Literal[ 'classifier', 'embedder' ] = 'embedder' # the name of the operation.
            'classifier' : identify the most accurate label for the entry using the majority voting strategy
            'embedder' : find an approximate embedding of the entry using the weighted averaging strategy
        axis : Union[ None, int, str ] = None # axis from which to retrieve X and y data. By default, the axis used for the knnindex model will be used.
        int_num_entries_in_a_batch : int = 10000 # the number of entries in a batch for each process. the larger the batch size is, the larger memory each process consumes.

        === embedder ===
        'float_std_ratio_for_outlier_detection' : float = 0.1 # when standard deviation of embeddings of the neighbor is larger than standard deviation values of the embeddings of all the points used in the KNN-index times this parameter, identify the point as an outlier.
            weighted-averaging will not be used for points that are classified as 'outliers' (very distant points identified as 'neighbors'). instead, the embedding of the closest point will be used.
        linkage_for_agglomerative_clustering_of_embeddings_of_neighbors : Literal[ 'single', 'complete', 'ward', 'average' ] = 'complete' # a method for calculating linkage for agglomerative clustering for identifying outliers
        flag_use_agglomerative_clustering_of_embeddings_of_neighbors_for_outlier_detection : bool = True # if set to 'True', use agglomerative clustering to identify outliers. if False, identify outliers by excluding neighbors based on the distance of the embeddings to the embedding of the closest neighbor

        === when reference ramdata is used ===
        int_index_component_reference : Union[ None, int ] = None # the index of the reference component RamData to use. By default, 'index_component_reference' attribute of the current RamData will be used.
        """
        """
        load the model and prepare 
        """
        # load the model and retrieve cluster labels
        type_model = "knnindex"
        model = self.load_model(name_model, type_model)
        if model is None:  # if the model does not exist, initiate the model
            if self.verbose:
                logger.info(
                    f"[RamData.apply_knn] the nearest-neighbor search index '{name_model}' does not exist, exiting"
                )
                return
        (
            flag_axis_is_barcode,
            int_num_nearest_neighbors_to_collect,
            name_col_x_knnindex,
            _,
            ba_filter_knnindex,
            knnindex,
            identifier,
            arr_neighbors,
            arr_neighbors_index,
        ) = (
            model["flag_axis_is_barcode"],
            model["int_num_nearest_neighbors_to_collect"],
            model["name_col_x"],
            model["int_num_components_x"],
            model["filter"],
            model["knnindex"],
            model["identifier"],
            model["arr_neighbors"] if "arr_neighbors" in model else None,
            model["arr_neighbors_index"] if "arr_neighbors_index" in model else None,
        )  # parse the model

        # handle inputs
        if axis is not None:  # set default axis
            flag_axis_is_barcode = self._determine_axis(
                axis
            )  # retrieve a flag indicating whether the data is summarized for each barcode or not # override settings from the loaded model
        # retrieve the axis
        ax = (
            self.bc if flag_axis_is_barcode else self.ft
        )  # retrieve the appropriate Axis object

        # retrieve flags
        flag_record_neighbors = (
            name_col_filter_neighbors_of_the_query is not None
        )  # a flag indicating whether to record neighbors

        # check whether the input column 'name_col_y_input' exists
        if name_col_y_input not in ax.meta:
            return

        # handle default 'name_col_y_output'
        if name_col_y_output is None:
            name_col_y_output = name_col_y_input

        # handle when input and output y columns are the same
        flag_name_col_y_input_and_output_are_same = (
            name_col_y_input == name_col_y_output
        )
        if flag_name_col_y_input_and_output_are_same:
            if self.verbose:
                logger.info(
                    "[RamData.apply_knn] 'name_col_y_input' and 'name_col_y_output' are the same. the input column will be overwritten."
                )

        # set default 'index_component_reference'
        if self.is_combined:
            if int_index_component_reference is None:
                int_index_component_reference = self.int_index_component_reference
        else:
            int_index_component_reference = None

        ba_filter_backup = (
            ax.filter
        )  # back up the bitarray filter before excluding entries used to build knnindex
        # set barcode filters excluding entries from the reference
        if int_index_component_reference is not None:
            ax.filter = (ax.all() if ax.filter is None else ax.filter) & (
                ~ax.select_component(int_index_component_reference)
            )  # exclude entries of the reference component

        """
        load the associated data objects
        """
        int_num_neighbors = knnindex.n_neighbors  # retrieve the number of neighbors

        # retrieve a setting for the number of nearest neighbors to use
        if (
            int_num_nearest_neighbors is None
            or int_num_nearest_neighbors > knnindex.n_neighbors
        ):
            int_num_nearest_neighbors = knnindex.n_neighbors

        # use name_col_x retrieved from 'knnindex' model by default
        if name_col_x is None:
            name_col_x = name_col_x_knnindex

        # check whether the input column 'name_col_x' exists
        if name_col_x not in ax.meta:
            return

        # retrieve the number of components for the model
        int_num_components_x = knnindex.dim

        # set filters for operation
        if name_col_filter_query is not None:
            self.change_filter(name_col_filter_query)

        # exclude entries used for building knnindex from the current filter
        if ax.filter is None:  # use all entries
            ax.filter = ax.all()

        # retrieve the entries used in knnindex
        if (
            identifier != self.identifier
        ):  # if the model did not originated from the current RamData, search the source RamData among the components
            # if 'combined' mode is not active, exit
            if not self.is_combined:
                if self.verbose:
                    logger.error(
                        "[RamData.apply_knn] model did not originated from the current RamData, and currently 'combined' mode is not active, exiting"
                    )
                return
            # search component ramdata with the identifier from the model
            int_index_component = None
            for index, ram in enumerate(self._l_ramdata):
                if ram.identifier == identifier:
                    int_index_component = (
                        index  # retrieve index of the matching component
                    )
                    break
            # if there is no component matching the identifier from the model, return
            if int_index_component is None:
                if self.verbose:
                    logger.error(
                        "[RamData.apply_knn] model did not originated from the current RamData or the direct component RamData objects, exiting"
                    )
                return

            # retrieve the entries used in knnindex, in a combined axis
            ba_filter_knnindex = ax.get_filter_combined_from_filter_component(
                ba_filter_knnindex, int_index_component
            )

        # if y_input and y_output are the same, exclude the entries used for training
        if flag_name_col_y_input_and_output_are_same:
            ax.filter = ax.filter & (~ba_filter_knnindex)

        # retrieve y values for the entries used for building knnindex
        y_knnindex = ax.meta[name_col_y_input, ba_filter_knnindex]

        # prepare for recording neighbors
        ns = dict()  # initialize a namespace
        int_num_entries_in_the_knnindex = (
            ba_filter_knnindex.count()
        )  # retrieve the number of entries in the knn index
        if flag_record_neighbors:
            # initialize a bitarray for recording neighbors
            ba_for_recording_neighbors = bitarray(int_num_entries_in_the_knnindex)
            ba_for_recording_neighbors.setall(0)
            ns["ba_for_recording_neighbors"] = ba_for_recording_neighbors

        # retrieve a flag indicating that the operation is embedding
        flag_embedder = operation == "embedder"

        # prepare
        if flag_embedder:  # %% EMBEDDER %%
            # calculate standard deviation of y values in order to identify outliers
            y_knnindex_std = y_knnindex.std(axis=0)
            y_std_threshold = float_std_ratio_for_outlier_detection * y_knnindex_std
            y_dist_threshold = math.sqrt(
                (y_std_threshold**2).sum()
            )  # calculate the distance threshold for detecting outliers (using euclidean distance)
            # initialize 'AgglomerativeClustering' instance
            if flag_use_agglomerative_clustering_of_embeddings_of_neighbors_for_outlier_detection:
                from sklearn.cluster import AgglomerativeClustering

        """
        assign labels or retrieve embeddings
        """
        if self.verbose:
            logging.info(
                f"[Info] [RamData.apply_label] the nearest-neighbor search started"
            )

        # define functions for multiprocessing step
        def process_batch(pipe_receiver_batch, pipe_sender_result):
            """# 2022-12-16 01:30:06"""

            # define functions
            def __find_label_with_largest_sum_of_weights(labels, weights):
                """# 2022-12-20 23:49:05
                fine labels with the largest sum of weights
                """
                # sum weights for each label
                dict_label_to_weight = dict()
                for label, weight in zip(labels, weights):
                    if label not in dict_label_to_weight:
                        dict_label_to_weight[label] = weight
                    else:
                        dict_label_to_weight[label] += weight
                return bk.DICTIONARY_Find_keys_with_max_value(dict_label_to_weight)[0][
                    0
                ]  # find the label with the maximum weight

            while True:
                batch = pipe_receiver_batch.recv()
                if batch is None:
                    break
                # parse the received batch
                int_num_of_previously_returned_entries, l_int_entry_current_batch = (
                    batch["int_num_of_previously_returned_entries"],
                    batch["l_int_entry_current_batch"],
                )

                # retrieve data from the axis metadata
                X = ax.meta[
                    name_col_x, l_int_entry_current_batch, :int_num_components_x
                ]

                neighbors, distances = knnindex.query(
                    X
                )  # retrieve neighbors using the index
                del X

                # use only 'int_num_nearest_neighbors' number of nearest neighbors
                if int_num_nearest_neighbors < knnindex.n_neighbors:
                    neighbors = neighbors[:, :int_num_nearest_neighbors]
                    distances = distances[:, :int_num_nearest_neighbors]

                # collect neighbors
                ba_neighbors = None
                if flag_record_neighbors:
                    # initialize a bitarray for recording neighbors
                    ba_neighbors = bitarray(int_num_entries_in_the_knnindex)
                    ba_neighbors.setall(0)
                    # collect neighbors
                    for e in set(neighbors.ravel()):
                        ba_neighbors[e] = True

                # knn-index based assignment of label/embedding
                l_res = []
                for neighbors_of_an_entry, distances_of_an_entry in zip(
                    neighbors, distances
                ):
                    # mark entries with zero distance
                    mask_zero_distance = distances_of_an_entry == 0
                    if (
                        mask_zero_distance
                    ).sum():  # if there is 'neighbor' with 0 distance, use the y of the 0-distance neighbor
                        res = y_knnindex[neighbors_of_an_entry][mask_zero_distance][
                            0
                        ]  # use the y of the first 0-distance neighbor (there should be at most 1 0-distance neighbor)
                    else:  # when there is no neighbors with 0-distance (all distance values should be larger than 0)
                        weights = (
                            1 / distances_of_an_entry
                        )  # calculate weights based on distances
                        if flag_embedder:  # %% EMBEDDER %%
                            y_knnindex_of_an_entry = y_knnindex[
                                neighbors_of_an_entry
                            ]  # retrieve y-values of an entry
                            if sum(
                                y_knnindex_of_an_entry.std(axis=0) > y_std_threshold
                            ):  # detect whether outliers are included in the neighbors (since knnindex is linear, but most embeddings are non-linear, knn-distance based method can identify very distant points in the embedding, and averaging these points should be avoided)
                                if flag_use_agglomerative_clustering_of_embeddings_of_neighbors_for_outlier_detection:
                                    ac = AgglomerativeClustering(
                                        n_clusters=None,
                                        distance_threshold=y_dist_threshold,
                                        linkage=linkage_for_agglomerative_clustering_of_embeddings_of_neighbors,
                                    )  # initialize the clustering instance
                                    arr_labels = ac.fit_predict(
                                        y_knnindex_of_an_entry
                                    )  # perform agglomerative clustering of the embeddings of the neighbors to exclude embeddings of the outliers
                                    mask_not_outlier = (
                                        arr_labels
                                        == __find_label_with_largest_sum_of_weights(
                                            arr_labels, weights
                                        )
                                    )  # retrieve the mask of neighbors belonging to the cluster with the largest sum of weights
                                else:
                                    # when very distant points are identified as 'neighbors', use the embedding of the closest point, in order to avoid weighted averaging of the embeddings including those of the distant points
                                    mask_not_outlier = (
                                        np.sqrt(
                                            (
                                                (
                                                    y_knnindex_of_an_entry
                                                    - y_knnindex_of_an_entry[0]
                                                )
                                                ** 2
                                            ).sum(axis=1)
                                        )
                                        < y_dist_threshold
                                    )  # retrieve points that are in the radius of the threshold distance from the closest point
                                # exclude embeddings of the outliers
                                weights = weights[mask_not_outlier]
                                y_knnindex_of_an_entry = y_knnindex_of_an_entry[
                                    mask_not_outlier
                                ]
                                if len(weights) == int_num_neighbors:
                                    print("outliers not filtered out")
                                    plt.plot(*y_knnindex_of_an_entry.T, ".")
                                    plt.show()
                            res = (y_knnindex_of_an_entry.T * weights).sum(
                                axis=1
                            ) / weights.sum()  # calculate weighted average of the y values for embedding mode
                        else:  # %% CLASSIFIER %%
                            res = __find_label_with_largest_sum_of_weights(
                                y_knnindex[neighbors_of_an_entry], weights
                            )  # find the label with the maximum weight
                    l_res.append(res)  # collect a result
                del neighbors, distances

                pipe_sender_result.send(
                    (l_int_entry_current_batch, l_res, ba_neighbors)
                )  # send the result back to the main process

        logger.info(
            f"Starting kNN-based {operation} operation using {int_num_entries_in_the_knnindex} entries in the index"
        )
        pbar = progress_bar(
            desc=f"{operation} using {int_num_entries_in_the_knnindex} entries",
            total=ax.meta.n_rows,
        )  # initialize the progress bar

        def post_process_batch(res):
            """# 2022-12-16 01:30:00"""
            # parse result
            l_int_entry_current_batch, l_res, ba_neighbors = res
            int_num_retrieved_entries = len(l_int_entry_current_batch)

            # write the result to the axis metadata
            ax.meta[name_col_y_output, l_int_entry_current_batch] = l_res

            if flag_record_neighbors:  # %% Collect neighbors %%
                ns[
                    "ba_for_recording_neighbors"
                ] |= ba_neighbors  # update the collected neighbors

            pbar.update(int_num_retrieved_entries)  # update the progress bar
            del l_res

        # transform values using iPCA using multiple processes
        bk.Multiprocessing_Batch_Generator_and_Workers(
            ax.batch_generator(
                ax.filter,
                int_num_entries_for_batch=int_num_entries_in_a_batch,
                flag_mix_randomly=False,
            ),
            process_batch,
            post_process_batch=post_process_batch,
            int_num_threads=int_num_threads,
            int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
        )
        pbar.close()  # close the progress bar

        if flag_record_neighbors:  # %% Collect neighbors %%
            l_int_entry = BA.to_integer_indices(
                ba_filter_knnindex
            )  # retrieve integer indices of the entries used for building knn index
            l_int_entry_of_collected_neighbors = list(
                l_int_entry[i] for i in BA.find(ns["ba_for_recording_neighbors"])
            )  # retrieve integer indices of the recorded neighbors

            # intialize the filter column
            ax.meta.initialize_column(
                name_col_filter_neighbors_of_the_query,
                dtype=bool,
                fill_value=False,
                dict_metadata_description={
                    "intended_function": "filter",
                    "intended_function.description": "record neighbors from knn search",
                },
            )
            # collect the secondary neighbors, too
            if (
                flag_include_secondary_neighbors_of_the_query
                and arr_neighbors is not None
            ):  # if flag has been set to True and valid 'arr_neighbors' is present
                set_int_entry_secondary_neighbors_of_the_query = (
                    set()
                )  # initialize the set
                for i in BA.find(
                    ns["ba_for_recording_neighbors"]
                ):  # for each entry in the knn index
                    set_int_entry_secondary_neighbors_of_the_query.update(
                        arr_neighbors[
                            arr_neighbors_index[i] : arr_neighbors_index[i + 1]
                        ]
                    )  # retrieve 'secondary' neighbors of the entry in the knnindex
                set_int_entry_secondary_neighbors_of_the_query.update(
                    l_int_entry_of_collected_neighbors
                )  # add 'primary' neighbors, the neighbor entries in the knnindex
                l_int_entry_of_collected_neighbors = np.sort(
                    list(set_int_entry_secondary_neighbors_of_the_query)
                )  # retrieve the sorted list of entries of collected neighbors

            ax.meta[
                name_col_filter_neighbors_of_the_query,
                l_int_entry_of_collected_neighbors,
            ] = True  # mark recorded neighbors to the filter

        # change back to the filter containing all target entries
        ax.filter = ba_filter_backup
        return

    """ deep-learning-based embedding/classification """

    def train_dl(
        self,
        # inputs
        name_model: str,
        name_col_x: str,
        name_col_y: str,
        name_col_filter_training: Union[str, None] = None,
        operation: Literal["classifier", "embedder"] = "embedder",
        axis: Union[int, str] = "barcodes",
        int_num_components_x: Union[None, int] = None,
        # preparing training dataset
        dict_kw_train_test_split={"test_size": 0.2, "random_state": 42},
        int_earlystopping_patience=5,
        # deep-learning model and training methods
        l_int_num_nodes=[
            100,
            90,
            85,
            75,
            50,
            25,
        ],  # by default 6 hiddle layers will be used
        float_rate_dropout=0.03,  # dropout ratio
        int_num_layers_for_each_dropout=6,  # dropout layer will be added for every this number of layers
        batch_size=400,
        epochs=100,
    ):
        """# 2023-02-17 18:49:21
        use deep-learning based model, built using Keras modules, to classify (predict labels) or embed (predict embeddings) entries.

        name_model : str # the name of the output model containing knn index
        name_col_x : str # the name of the column containing X (input) data
        name_col_filter_training : str # the name of column containing filter for entries that will be used for training
        operation : Literal[ 'classifier', 'embedder' ] = 'embedder' # 'classifier' for classification (e.g. leiden label assignment) and 'embedder' for embedding (e.g. learning PCA -> UMAP/tSNE representation mapping)
        axis : Union[ int, str ] = 'barcodes' # axis from which to retrieve X
        int_num_components_x : Union[ None, int ] = None # by default, use all components available in X
        n_neighbors : int = 10 # the number of neighbors to use
        dict_kw_pynndescent : dict = { 'low_memory' : True, 'n_jobs' : None, 'compressed' : False } # the additional keyworded arguments for pynndescent index
        """
        import tensorflow as tf
        from sklearn.model_selection import train_test_split
        from tensorflow.keras import layers

        # handle inputs
        flag_axis_is_barcode = axis in {
            0,
            "barcode",
            "barcodes",
        }  # retrieve a flag indicating whether the data is summarized for each barcode or not

        ax = (
            self.bc if flag_axis_is_barcode else self.ft
        )  # retrieve the appropriate Axis object

        # set filters for operation
        if name_col_filter_training is not None:
            self.change_or_save_filter(name_col_filter_training)

        # exit if the input columns do not exist
        if name_col_x not in ax.meta:
            logger.error(f"[RamData.train_dl] {name_col_x} column does not exist")
            return
        if name_col_y not in ax.meta:
            logger.error(f"[RamData.train_dl] {name_col_y} column does not exist")
            return

        # check validity of operation
        if operation not in {"classifier", "embedder"}:
            logger.error(f"[RamData.train_dl] '{operation}' operation is invalid")
            return

        # check whether the model of the given name already exists
        type_model = f"deep_learning.keras.{operation}"
        if self.check_model(name_model, type_model):  # if the model exists, return
            logger.info(
                f"[RamData.train_dl] the model '{name_model}' for '{operation}' operation already exists, exiting"
            )
            return

        """
        retrieve data
        """
        # load X
        if int_num_components_x is None:
            shape_secondary = self.bc.meta.get_shape(name_col_x)
            assert (
                len(shape_secondary) > 0
            )  # more than single component should be available as an input data
            X = ax.meta[name_col_x]  # load all components
        else:
            X = ax.meta[
                name_col_x, None, :int_num_components_x
            ]  # load top 'int_num_components_x' number of components
        # load y
        y = ax.meta[name_col_y]

        """
        train model for each operation
        """
        # retrieve a flag indicating that the operation is embedding
        flag_embedder = operation == "embedder"

        # prepare y
        if flag_embedder:
            # %% EMBEDDER %%
            # scale y
            y_min, y_max = y.min(axis=0), y.max(axis=0)  # retrieve min and max values
            y = (y - y_min) / (y_max - y_min)  # scale the 'y' from 0 to 1
        else:
            # %% CLASSIFIER %%
            l_unique_labels = sorted(set(y))  # retrieve list of unique labels
            dict_label_to_int_label = dict(
                (label, int_label) for int_label, label in enumerate(l_unique_labels)
            )  # retrieve mapping from label to integer representation of label
            y_one_hot_encoding = np.zeros(
                (len(y), len(l_unique_labels)), dtype=bool
            )  # initialize y for encoding labels
            # perform one-hot-encoding
            for index, label in enumerate(y):
                y_one_hot_encoding[index, dict_label_to_int_label[label]] = True
            y = y_one_hot_encoding  # use one-hot-encoded y as y
            del y_one_hot_encoding

        # setting for a neural network
        int_num_components_x = X.shape[1]

        # initialize sequential model
        model = tf.keras.Sequential()

        # add hiddle dense layers according to the setting
        for index_layer, int_num_nodes in enumerate(l_int_num_nodes):
            model.add(layers.Dense(int_num_nodes))
            model.add(layers.Activation("relu"))
            if float_rate_dropout > 0:
                if index_layer % int_num_layers_for_each_dropout == 0:
                    model.add(layers.Dropout(float_rate_dropout))

        # add final output layer according to each operation
        if flag_embedder:
            # %% EMBEDDER %%
            model.add(layers.Dense(y.shape[1]))
            model.add(layers.Activation("sigmoid"))
            model.compile(
                loss="mean_absolute_error", optimizer="adam", metrics=["accuracy"]
            )
        else:
            # %% CLASSIFIER %%
            model.add(layers.Dense(len(y[0])))
            model.add(layers.Activation("softmax"))
            model.compile(
                loss="categorical_crossentropy",
                optimizer="adam",
                metrics=[tf.keras.metrics.AUC(), "accuracy"],
            )

        # build and print model
        model._name = name_model
        model.build(input_shape=(1, int_num_components_x))
        model.summary()

        # split test/training dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, **dict_kw_train_test_split
        )  # split train/test dataset

        # start training
        # mirrored_strategy = tf.distribute.MirroredStrategy( ) # distributed training
        # with mirrored_strategy.scope( ) :
        earlystopper = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=int_earlystopping_patience, verbose=1
        )  # earlystopper to prevent overfitting

        with tf.device("/CPU:0"):
            # avoid a known bug in a tensorflow trying to fit an entire dataset into GPU memory by converting it to tensor before running model.fit
            X_train = tf.convert_to_tensor(X_train)
            X_test = tf.convert_to_tensor(X_test)
            y_train = tf.convert_to_tensor(y_train)
            y_test = tf.convert_to_tensor(y_test)

        model.fit(
            X_train,
            y_train,
            batch_size=batch_size,
            epochs=epochs,
            shuffle=True,
            validation_data=(X_test, y_test),
            callbacks=[earlystopper],
        )

        # save trained model # collect metadata of the output columns
        dict_model = {
            "name_col_x": name_col_x,
            "name_col_y": name_col_y,
            "int_num_components_x": int_num_components_x,
            "dict_kw_train_test_split": dict_kw_train_test_split,
            "flag_axis_is_barcode": flag_axis_is_barcode,
            "filter": ax.filter,
            "dl_model": model,
            "metadata_col_x": ax.meta.initialize_column(
                name_col=None,
                name_col_template=name_col_x,
                flag_dry_run=True,
            ),
            "metadata_col_y": ax.meta.initialize_column(
                name_col=None,
                name_col_template=name_col_y,
                flag_dry_run=True,
            ),
        }
        # collect metadata for reconstructing y from the output of the model
        if flag_embedder:
            # %% EMBEDDER %%
            dict_model.update({"y_min": y_min, "y_max": y_max})
        else:
            # %% CLASSIFIER %%
            dict_model.update(
                {
                    "l_unique_labels": l_unique_labels,
                    "dict_label_to_int_label": dict_label_to_int_label,
                }
            )
        self.save_model(
            dict_model, name_model, type_model
        )  # save model and associated metadata

        # report
        if self.verbose:
            logger.info(
                f"[Info] [RamData.train_dl] deep learning {operation} training completed for {ax.meta.n_rows} number of entries of the axis '{'barcodes' if flag_axis_is_barcode else 'features'}' using the data from the column '{name_col_x}' as X and '{name_col_y}' as y"
            )

    def apply_dl(
        self,
        name_model: str,
        name_col_y: str,
        operation: Literal["classifier", "embedder"] = "embedder",
        name_col_x: Union[str, None] = None,
        name_col_filter_target: Union[str, None] = None,
        flag_apply_to_entries_used_for_training: bool = True,
        axis: Union[int, str, None] = None,
        int_num_entries_in_a_batch: int = 500000,
        int_num_threads: int = 3,
        int_index_component_reference: Union[None, int] = None,
    ):
        """# 2022-09-15 21:33:18
        use deep-learning based model, built using Keras modules, to classify (predict labels) or embed (predict embeddings) entries.

        name_model : str # the name of the model containing knn index
        name_col_y : str # the name of the column containing y (output) data. Of note, since deep-learning often do not reproduce the output accurately,
            it is recommended to map both the entries used for training and not used for training to output values. Therefore, a new column name that will contains deep-learning predicted values is recommended.
        name_col_x : Union[ str, None ] # the name of the column containing X (input) data. by default (if None is given), name_col_x stored in the model will be used.
        name_col_filter_target : str # the name of column containing filter for entries to which the model will be applied
        operation : Literal[ 'classifier', 'embedder' ] = 'embedder' # the name of the operation.
            'classifier' : predict the label with the best score from deep-learning model
            'embedder' : retrieve embedding using the deep-learning model
        axis : Union[ int, str, None ] = None # axis from which to retrieve X and y data.
        int_num_entries_in_a_batch : int = 10000 # the number of entries in a batch for each process. the larger the batch size is, the larger memory each process consumes.
        int_num_threads : int = 10 # the number of threads to use for applying the model
        flag_apply_to_entries_used_for_training : bool = True # if True, entries used for training will be also included in the entries to which deep-learning-based model will be applied. It is recommended to map both the entries used for training and not used for training to output values, and thus the default setting of this argument is True.
            To prevent modification of the original data used for training, when

        === when reference ramdata is used ===
        int_index_component_reference : Union[ None, int ] = None # the index of the reference component RamData to use. By default, 'index_component_reference' attribute of the current RamData will be used.
        """
        """ load the model """
        # check validity of operation
        if operation not in {"classifier", "embedder"}:
            logger.error(f"[RamData.apply_dl] '{operation}' operation is invalid")
            return

        # check whether the model of the given name already exists
        type_model = f"deep_learning.keras.{operation}"
        if not self.check_model(
            name_model, type_model
        ):  # if the model does not exist, return
            logger.error(
                f"[RamData.apply_dl] the model '{name_model}' for '{operation}' operation does not exist, exiting"
            )
            return
        model = self.load_model(name_model, type_model)
        dl_model = model.pop("dl_model")

        """ retrieve the default model """
        # set axis
        if axis is None:
            flag_axis_is_barcode = model[
                "flag_axis_is_barcode"
            ]  # by default, the axis used for training will be used
        else:
            flag_axis_is_barcode = axis in {
                0,
                "barcode",
                "barcodes",
            }  # retrieve a flag indicating whether the data is summarized for each barcode or not
        ax = (
            self.bc if flag_axis_is_barcode else self.ft
        )  # retrieve the appropriate Axis object

        # set default 'index_component_reference'
        if self.is_combined:
            if int_index_component_reference is None:
                int_index_component_reference = self.int_index_component_reference
        else:
            int_index_component_reference = None

        # set filters for operation
        if name_col_filter_target is not None:
            self.change_filter(name_col_filter_target)

        ba_filter_backup = ax.filter  # backup the filter before modifying the filter
        # set barcode filters excluding entries from the reference
        if int_index_component_reference is not None:
            ax.filter = (ax.all() if ax.filter is None else ax.filter) & (
                ~ax.select_component(int_index_component_reference)
            )  # exclude entries of the reference component

        # set default input/output column names
        if name_col_x is None:
            name_col_x = model["name_col_x"]
        if name_col_y is None:
            name_col_y = model["name_col_y"]

        # if name_col of the y used for training is same as the name of column of the y for writing output, automatically exclude entries used for training from generating output and thus overwritting the original values
        if name_col_y == model["name_col_y"]:
            flag_apply_to_entries_used_for_training = False

        # exit if the input columns do not exist
        if name_col_x not in ax.meta:
            logger.error(f"[RamData.train_dl] {name_col_x} column does not exist")
            return
        # if the output column does not exist, initialize the 'y' output column using the 'y' column used for training.
        if name_col_y not in ax.meta:
            if model["name_col_y"] not in ax.meta:
                logger.info(
                    f"[RamData.train_dl] '{name_col_y}' output column will be initialized with the existing metadata of the '{model[ 'name_col_y' ]}' column"
                )
                ax.meta.initialize_column(
                    name_col=name_col_y,
                    data_for_initialization=model[
                        "metadata_col_y"
                    ],  # use the retrieved metadata of the output column
                )  # initialize the output column using the settings from the y column used for training.
            else:
                logger.info(
                    f"[RamData.train_dl] '{name_col_y}' output column will be initialized with '{model[ 'name_col_y' ]}' column"
                )
                ax.meta.initialize_column(
                    name_col_y, name_col_template=model["name_col_y"]
                )  # initialize the output column using the settings from the y column used for training.

        # exclude entries used for building knnindex from the current filter
        if not flag_apply_to_entries_used_for_training:
            ax.filter = ax.filter & (
                ~model["filter"]
            )  # exclude the entries used for training the model

        # retrieve 'int_num_components_x'
        int_num_components_x = model["int_num_components_x"]

        # retrieve a flag indicating that the operation is embedding
        flag_embedder = operation == "embedder"

        """
        assign labels or retrieve embeddings
        """
        if self.verbose:
            logger.info(f"[RamData.apply_dl] applying deep-learning model started")

        # define functions for multiprocessing step
        def process_batch(pipe_receiver_batch, pipe_sender_result):
            """# 2022-09-06 17:05:15"""
            # retrieve fork-safe zarr object
            za_fork_safe = ax.meta.get_zarr(
                name_col_x
            )  # retrieve zarr object or zarr-server object according to the axis setting (whether the axis includes remote dataset)

            while True:
                batch = pipe_receiver_batch.recv()
                if batch is None:
                    break
                # parse the received batch
                int_num_of_previously_returned_entries, l_int_entry_current_batch = (
                    batch["int_num_of_previously_returned_entries"],
                    batch["l_int_entry_current_batch"],
                )

                # retrieve data from the axis metadata
                X = za_fork_safe.get_orthogonal_selection(
                    (l_int_entry_current_batch, slice(None, int_num_components_x))
                )
                pipe_sender_result.send(
                    (l_int_entry_current_batch, X)
                )  # send the result back to the main process

            # dismiss fork-safe zarr object
            za_fork_safe.terminate()  # shutdown the zarr server

        pbar = progress_bar(
            desc=f"deep-learning {operation}", total=ax.meta.n_rows
        )  # initialize the progress bar

        def post_process_batch(res):
            """# 2022-07-13 22:18:26"""
            # parse result
            l_int_entry_current_batch, X = res
            int_num_retrieved_entries = len(l_int_entry_current_batch)

            # predict using the deep-learning model
            arr_y = dl_model.predict(X)

            # post-process the result to retrieve the output values
            if flag_embedder:
                # %% EMBEDDER %%
                # scale back the output to input values
                arr_y_scaled = (
                    arr_y * (model["y_max"] - model["y_min"]) + model["y_min"]
                )
                l_res = arr_y_scaled
                del arr_y_scaled
            else:
                # %% CLASSIFIER %%
                l_unique_labels = model["l_unique_labels"]
                arr_labels = np.zeros(
                    len(arr_y), dtype=object
                )  # intialize an array to contain labels
                for index, int_label in enumerate(
                    arr_y.argmax(axis=1)
                ):  # retrieve predicted label for each entry
                    arr_labels[index] = l_unique_labels[int_label]
                l_res = arr_labels
                del arr_labels
            del arr_y

            # write the result to the axis metadata
            ax.meta[name_col_y, l_int_entry_current_batch] = l_res

            pbar.update(int_num_retrieved_entries)  # update the progress bar
            del l_res

        # transform values using iPCA using multiple processes
        bk.Multiprocessing_Batch_Generator_and_Workers(
            ax.batch_generator(
                ax.filter,
                int_num_entries_for_batch=int_num_entries_in_a_batch,
                flag_mix_randomly=False,
            ),
            process_batch,
            post_process_batch=post_process_batch,
            int_num_threads=int_num_threads,
            int_num_seconds_to_wait_before_identifying_completed_processes_for_a_loop=0.2,
        )

        # close the progress bar
        pbar.close()

        # change back to the filter containing all target entries
        ax.filter = ba_filter_backup
        return

    """ for marker detection analysis """

    def find_markers(
        self,
        name_layer: str = "normalized_log1p_scaled",
        name_col_label: str = "subsampling_label",
        index_name_col_label: int = -1,
        l_name_cluster: Union[list, np.ndarray, tuple, set, None] = None,
        name_col_auroc: str = "marker_auroc",
        name_col_log2fc: str = "marker_log2fc",
        name_col_pval: str = "marker_pval",
        method_pval: str = "wilcoxon",
        int_chunk_size_secondary=10,
    ):
        """# 2022-08-21 13:37:02
        find marker features for each cluster label by calculating a AUROC metric, log2FC, and Wilcoxon (or alternatively, t-test or Mann-Whitney-U rank test)

        name_layer : str = 'normalized_log1p_scaled' : a layer containing expression data to use for finding marker. scaled data is recommended
        name_col_label : str = 'subsampling_label' : the name of the column of 'barcodes' metadata containing cluster labels
        index_name_col_label : int = -1 : the index of the column (secondary axis) of the 'name_col_label' metadata column. if no secondary axis is available, this argument will be ignored.
        l_name_cluster : Union[ list, np.ndarray, tuple, None ] = None : the list of cluster labels that will be included


        === output ===
        name_col_auroc : str = 'marker_auroc' : the name of the output column name in the 'features' metadata ZDF. This column contains Area Under Receiver Operating Characteristic (Sensitivity/Specificity) curve values for each cluster and feature pair. if None is given, AUROC will be not calculated
        name_col_log2fc : str = 'marker_log2fc' : the name of the output column name in the 'features' metadata ZDF. This column contains Log_2 fold change values of the cells of the cluster label of interest versus the rest of the cells.
        name_col_pval : str = 'marker_pval' : the name of the output column name in the 'features' metadata ZDF. This column contains uncorrected p-value from the wilcoxon or t-test results
        method_pval : str = 'wilcoxon' : one of the test methods in { 'wilcoxon', 't-test', 'mann-whitney-u' }
        int_chunk_size_secondary : int = 10 : the chunk size of the output columns along the secondary axis

        an array with a shape of ( the number of all features ) X ( the number of all cluster labels ), stored in the feature metadata using the given column name
        information about which column of the output array represent which cluster label is available in the column metadata.
        """
        from sklearn.metrics import roc_auc_score
        import scipy.stats

        # handle inputs
        if name_col_label not in self.bc.meta:  # check input label
            if self.verbose:
                logger.error(
                    f"[RamData.find_markers] 'name_col_label' {name_col_label} does not exist in barcode metadata, exiting"
                )
            return

        if name_layer not in self.layers:  # check input layer
            if self.verbose:
                logger.error(
                    f"[RamData.find_markers] 'name_layer' {name_layer} does not exist in the layers, exiting"
                )
            return
        self.layer = name_layer  # load layer

        # retrieve flags
        flag_calcualte_auroc = name_col_auroc is not None
        flag_calculate_pval = name_col_pval is not None
        assert name_col_log2fc is not None  # 'name_col_log2fc' should not be None

        # retrieve function for testing p-value
        test = None
        if flag_calculate_pval:
            if method_pval not in {"wilcoxon", "t-test", "mann-whitney-u"}:
                if self.verbose:
                    logger.error(
                        f"[RamData.find_markers] 'method_pval' {method_pval} is invalid, exiting"
                    )
                return
            if method_pval == "t-test":
                test = scipy.stats.ttest_ind
            elif method_pval == "wilcoxon":
                test = scipy.stats.ranksums
            elif method_pval == "mann-whitney-u":
                test = scipy.stats.mannwhitneyu

        # compose 'l_name_col_summarized', a list of output column names
        l_name_col_summarized = [name_col_log2fc]
        l_fill_value = [np.nan]  # for 'col_log2fc', fill_value = 0
        if flag_calcualte_auroc:
            l_name_col_summarized.append(name_col_auroc)
            l_fill_value.append(0)
        if flag_calculate_pval:
            l_name_col_summarized.append(name_col_pval)
            l_fill_value.append(-1)

        # retrieve labels (considering filters)
        n_dims_non_primary = len(self.bc.meta.get_shape(name_col_label))
        arr_cluster_label = (
            self.bc.meta[name_col_label]
            if n_dims_non_primary == 0
            else self.bc.meta[name_col_label, None, index_name_col_label]
        )  # retrieve cluster labels
        int_num_barcodes = len(
            arr_cluster_label
        )  # retrieve the number of active barcodes
        l_unique_cluster_label = sorted(
            convert_numpy_dtype_number_to_number(e) for e in set(arr_cluster_label)
        )  # retrieve a list of unique cluster labels
        dict_cluster_label_to_index = dict(
            (e, i) for i, e in enumerate(l_unique_cluster_label)
        )  # map cluster labels to integer indices
        int_num_cluster_labels = len(
            l_unique_cluster_label
        )  # retrieve the total number of cluster labels

        if (
            l_name_cluster is not None
        ):  # if 'l_name_cluster' is given, analyze only the labels in the given list of cluster labels
            set_cluster_label = set(l_name_cluster)
            l_unique_cluster_label_to_analyze = list(
                e for e in l_unique_cluster_label if e in set_cluster_label
            )
            del set_cluster_label
        else:  # by default, analyze all cluster labels
            l_unique_cluster_label_to_analyze = l_unique_cluster_label

        # initialize output columns
        for name_col, fill_value in zip(
            l_name_col_summarized, l_fill_value
        ):  # for each column, retrieve name_col and fill_value
            name_col = (
                f"{name_layer}_{name_col}"  # compose the name of the destination column
            )
            self.ft.meta.initialize_column(
                name_col,
                dtype=np.float64,
                shape_not_primary_axis=(int_num_cluster_labels,),
                chunks=(int_chunk_size_secondary,),
                fill_value=fill_value,
            )
            dict_metadata = self.ft.meta.get_column_metadata(
                name_col
            )  # retrieve metadata
            dict_metadata[
                "l_labels_1"
            ] = l_unique_cluster_label  # add cluster label information
            self.ft.meta.set_column_metadata(
                name_col, dict_metadata
            )  # update column metadata

        # create view
        flag_view_was_not_active = (
            not self.bc.is_view_active
        )  # retrieve a flag indicating a view was not active
        if flag_view_was_not_active:  # create view
            self.bc.create_view()

        def func(
            self,
            int_entry_of_axis_for_querying: int,
            arr_int_entries_of_axis_not_for_querying: np.ndarray,
            arr_value: np.ndarray,
        ):  # normalize count data of a single feature containing (possibly) multiple barcodes
            """# 2022-08-22 11:25:57
            find markers
            """
            if (
                len(arr_value) == 0
            ):  # handle when no expression values are available, exit
                return

            dict_summary = dict(
                (name_col, [fill_value] * int_num_cluster_labels)
                for name_col, fill_value in zip(l_name_col_summarized, l_fill_value)
            )  # initialize output dictionary

            arr_expr = np.zeros(
                int_num_barcodes
            )  # initialize expression values in dense format
            arr_expr[
                arr_int_entries_of_axis_not_for_querying
            ] = arr_value  # convert sparse to dense format

            # for each cluster
            for name_clus in l_unique_cluster_label_to_analyze:
                index_clus = dict_cluster_label_to_index[
                    name_clus
                ]  # retrieve index of the current cluster
                # retrieve expression values of cluster and the rest of the barcodes
                mask = arr_cluster_label == name_clus
                arr_expr_clus = arr_expr[mask]
                arr_expr_rest = arr_expr[~mask]

                # calculate log2fc values
                mean_arr_expr_rest = arr_expr_rest.mean()
                if mean_arr_expr_rest != 0:
                    try:
                        dict_summary[name_col_log2fc][index_clus] = math.log2(
                            arr_expr_clus.mean() / mean_arr_expr_rest
                        )
                    except ValueError:  # catch math.log2 domain error
                        pass

                # calculate auroc
                if flag_calcualte_auroc:
                    dict_summary[name_col_auroc][index_clus] = roc_auc_score(
                        mask, arr_expr
                    )

                # calculate ttest
                if flag_calculate_pval and test is not None:
                    dict_summary[name_col_pval][index_clus] = test(
                        arr_expr_clus, arr_expr_rest
                    ).pvalue
            return dict_summary

        # report
        if self.verbose:
            logger.info(
                f"[RamData.find_markers] finding markers for {len( l_unique_cluster_label_to_analyze )} number of clusters started"
            )

        # calculate the metric for identifying marker features
        self.summarize(
            name_layer, "features", func, l_name_col_summarized=l_name_col_summarized
        )

        # destroy view if a view was not active
        if flag_view_was_not_active:
            self.bc.destroy_view()

        # report
        if self.verbose:
            logger.info(
                f"[RamData.find_markers] [Info] finding markers for {len( l_unique_cluster_label_to_analyze )} number of clusters completed"
            )

    def get_marker_table(
        self,
        max_pval: float = 1e-10,
        min_auroc: float = 0.7,
        min_log2fc: float = 1,
        name_col_auroc: Union[str, None] = None,
        name_col_log2fc: Union[str, None] = None,
        name_col_pval: Union[str, None] = None,
        int_num_chunks_in_a_batch: int = 10,
    ):
        """# 2023-01-19 01:18:51
        retrieve marker table using the given thresholds

        === arguments ===
        max_pval : float = 1e-10 : maximum p-value for identification of marker features
        min_auroc : float = 0.7 : minimum AUROC metric value for identification of marker features
        min_log2fc : float = 1 : minimum Log2 fold change metric value for identification of marker features
        name_col_auroc : Union[ str, None ] = 'normalized_log1p_scaled_marker_auroc' : the name of the column containing AUROC metrics for each feature for each cluster label. if None is given, AUROC metric will be ignored
        name_col_log2fc : Union[ str, None ] = 'normalized_log1p_scaled_marker_log2fc' : the name of the column containing AUROC metrics for each feature for each cluster label. if None is given, Log2FC values will be ignored
        name_col_pval : Union[ str, None ] = 'normalized_log1p_scaled_marker_pval' : the name of the column containing p-value significance for null-hypothesis testing for each feature for each cluster label. if None is given, p-value will be ignored
        int_num_chunks_in_a_batch : int = 10 : the number of chunks in a batch
        """
        # retrieve the maximum number of entries in a batch
        int_num_entries_in_a_batch = (
            self.ft.meta.get_int_num_rows_in_a_chunk(np.float64)
            * int_num_chunks_in_a_batch
        )  # use the number of rows in a chunk when using np.float64 dtype

        # handle inputs
        flag_use_auroc = name_col_auroc is not None
        flag_use_log2fc = name_col_log2fc is not None
        flag_use_pval = name_col_pval is not None

        if not (flag_use_auroc or flag_use_log2fc or flag_use_pval):
            if self.verbose:
                logger.error(
                    f"[RamData.get_marker_table] at least one metric should be used for filtering markers but none were given, exiting."
                )
            return

        # retrieve 'features' axis
        ax = self.ft

        # retrieve a list of unique cluster labels
        flag_column_identified = False
        for name_col in [name_col_auroc, name_col_log2fc, name_col_pval]:
            if name_col in ax.meta:
                l_unique_cluster_label = ax.meta.get_column_metadata(name_col)[
                    "l_labels_1"
                ]
                flag_column_identified = True
                break
        if not flag_column_identified:
            if self.verbose:
                logger.error(
                    f"[RamData.get_marker_table] no column with cluster labels was identified, exiting."
                )
            return
        # retrieve the number of cluster labels
        int_num_cluster_labels = len(l_unique_cluster_label)

        # collect the result
        l_l = []

        int_num_entries_searched = 0  # initialize the position
        int_num_entries_total = (
            self.ft.int_num_entries
        )  # retrieve the total number of entries to search
        while (
            int_num_entries_searched <= int_num_entries_total
        ):  # until all entries were searched
            mask = np.ones(
                (
                    min(
                        int_num_entries_in_a_batch,
                        int_num_entries_total - int_num_entries_searched,
                    ),
                    int_num_cluster_labels,
                ),
                dtype=bool,
            )  # initialize the mask # include all records by default
            sl = slice(
                int_num_entries_searched, int_num_entries_searched + mask.shape[0]
            )  # retrieve a slice for the batch
            if flag_use_auroc:
                arr_data = ax.meta[name_col_auroc, sl, :]  # retrieve data
                mask &= arr_data >= min_auroc  # apply filter using AUROC metrics
                arr_data_auroc = arr_data
            if flag_use_log2fc:
                arr_data = ax.meta[name_col_log2fc, sl, :]  # retrieve data
                mask &= ~np.isnan(arr_data)  # apply filter using valid log2fc values
                mask &= arr_data >= min_log2fc  # apply filter using log2fc values
                arr_data_log2fc = arr_data
            if flag_use_pval:
                arr_data = ax.meta[name_col_pval, sl, :]  # retrieve data
                mask &= arr_data != -1  # apply filter using valid p-values
                mask &= arr_data <= max_pval  # apply filter using p-values
                arr_data_pval = arr_data

            # retrieve coordinates of filtered records
            coords_filtered = np.where(mask)
            int_num_records_filtered = len(
                coords_filtered[0]
            )  # retrieve the number of records after filtering for the current batch

            # retrieve data of filtered records
            arr_data_auroc = (
                arr_data_auroc[coords_filtered]
                if flag_use_auroc
                else np.full(int_num_records_filtered, np.nan)
            )
            arr_data_log2fc = (
                arr_data_log2fc[coords_filtered]
                if flag_use_log2fc
                else np.full(int_num_records_filtered, np.nan)
            )
            arr_data_pval = (
                arr_data_pval[coords_filtered]
                if flag_use_pval
                else np.full(int_num_records_filtered, np.nan)
            )

            (
                arr_int_entry_ft_filtered,
                arr_int_name_cluster_filtered,
            ) = coords_filtered  # parse coordinates
            arr_int_entry_ft_filtered += (
                int_num_entries_searched  # correct 'arr_int_entry_ft_filtered'
            )
            for (
                int_entry_ft,
                int_name_cluster,
                value_auroc,
                value_log2fc,
                value_pval,
            ) in zip(
                arr_int_entry_ft_filtered,
                arr_int_name_cluster_filtered,
                arr_data_auroc,
                arr_data_log2fc,
                arr_data_pval,
            ):  # for each record
                l_l.append(
                    [
                        int_entry_ft,
                        l_unique_cluster_label[int_name_cluster],
                        value_auroc,
                        value_log2fc,
                        value_pval,
                    ]
                )  # collect metrics and cluster label

            int_num_entries_searched += int_num_entries_in_a_batch  # update positions
        df_marker = pd.DataFrame(
            l_l,
            columns=[
                "name_feature",
                "name_cluster",
                "value_auroc",
                "value_log2fc",
                "value_pval",
            ],
        )  # retrieve marker table as a dataframe
        if len(df_marker) == 0:  # handle the case when no records exist after filtering
            return df_marker

        arr_int_entry_ft = np.sort(
            df_marker.name_feature.unique()
        )  # retrieve integer representation of features
        arr_str_entry_ft = self.ft.get_str(
            arr_int_entry_ft
        )  # retrieve string representations of the features
        dict_mapping = dict(
            (i, s) for i, s in zip(arr_int_entry_ft, arr_str_entry_ft)
        )  # retrieve a mapping of int > str repr. of features
        df_marker["name_feature"] = list(
            dict_mapping[i] for i in df_marker["name_feature"].values
        )  # retrieve string representations of the features of the marker table
        return df_marker

    """ exploration & visualization functions """
    def get_word_count( 
        self,
        axis : Union[ int, str ] = 'barcodes',
        l_name_col : Union[ None, List ] = None,
        l_l_query : Union[ None, List[ List ] ] = [ [ 'cell_type', '-ontology' ], [ 'celltype', '-ontology' ] ],
        name_col_group : Union[ None, str ] = None,
        l_stop_words : List = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'of', 'the', '', 'cell', 'cells' ],
        l_delimitors : List = [ ',', ' ', ';', '_', '/' ],
    ) :
        """ # 2023-05-11 19:57:57 
        retrieve word count of a given list of columns of the given axis containing string categorical values. The resulting word count can be used to draw word cloud

        axis : Union[ int, str ] = 'barcodes', # axis from which to collect the metadata
        l_name_col : Union[ None, List ] = None, # the list of name_col to collect the metadata (categorical data)
        l_l_query : Union[ None, List[ List ] ] = [ [ 'cell_type', '-ontology' ], [ 'celltype', '-ontology' ] ], # list of queries to perform the search to collect the metadata
        name_col_group : Union[ None, str ] = None, # the name of the column containing categorical data. The word count dictionary will be obtained for each categorical label of the column. if None is given, the word count dictionary will be obtained for all active entries.
        l_stop_words : List = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'of', 'the', '', 'cell', 'cells' ], # list of stop words (the words that will be ignored when counting words)
        l_delimitors : List = [ ',', ' ', ';', '_', '/' ], # list of characters to use when separating the categorical labels in the metadata to obtain the word count data.
        """
        # determine the axis
        flag_axis_is_barcode = self._determine_axis( axis )
        ax = self.bc if flag_axis_is_barcode else self.ft # retrieve the axis

        # retrieve 'l_name_col'
        if l_name_col is None : # if 'l_name_col' is not given, retrieve list of name_col using the queries
            if l_l_query is None :
                raise KeyError( "No columns have been specified to retrieve categorical string data. Please set either 'l_name_col' or 'l_l_query'" )
            set_name_col = set( )
            for l_query in l_l_query :
                set_name_col.update( self.bc.search_columns( * l_query ) )
            l_name_col = list( set_name_col ) # retrieve list of columns

        # retrieve groups
        flag_group_is_used = False
        if name_col_group is not None : # if the group
            l_group = ax.meta.get_categories( name_col_group ) # retrieve categories that will be used to group entries
            if len( l_group ) > 0 : # if valid categories exist
                flag_group_is_used = True
                arr_group = ax.meta.get_categorical_data_as_integers( name_col_group ) # retrieve data

        # prepare
        set_stop_words = set( l_stop_words )
        str_delim_universal = '1fcf2a7f0cf04246a6dbb089256c16e2' # a string that will be used as a universal delimiter

        # count words for each column
        for name_col in l_name_col : # for each column
            l_cat = ax.meta.get_categories( name_col ) # retrieve categories        
            if len( l_cat ) > 0 : # if valid categories exist
                # count word for each category
                l_dict_word_count_cat = [ ]
                for cat in l_cat :
                    for delim in l_delimitors :
                        if delim in cat :
                            cat = cat.replace( delim, str_delim_universal )
                    dict_count = bk.COUNTER( cat.split( str_delim_universal ) )
                    dict_count = dict( ( e, dict_count[ e ] ) for e in dict_count if e not in set_stop_words )
                    l_dict_word_count_cat.append( dict_count )

                if flag_group_is_used : # count words for each group by iterating the entries
                    dict_int_group_to_dict_word_count = dict( )
                    for int_cat, int_group in zip( ax.meta.get_categorical_data_as_integers( name_col ), arr_group ) : # int_category, int_group of each entry
                        if int_group not in dict_int_group_to_dict_word_count :
                            dict_int_group_to_dict_word_count[ int_group ] = dict( )
                        if int_cat == -1 : # ignore NaN values
                            continue
                        # update word count
                        dict_word_count_cat = l_dict_word_count_cat[ int_cat ] # retrieve the word count of the category
                        for word in dict_word_count_cat :
                            if word not in dict_int_group_to_dict_word_count[ int_group ] :
                                dict_int_group_to_dict_word_count[ int_group ][ word ] = dict_word_count_cat[ word ]
                            else :
                                dict_int_group_to_dict_word_count[ int_group ][ word ] += dict_word_count_cat[ word ]
                else :
                    dict_word_count = dict( )
                    for int_cat in ax.meta.get_categorical_data_as_integers( name_col ) : # int_category of each entry
                        if int_cat == -1 : # ignore NaN values
                            continue
                        # update word count
                        dict_word_count_cat = l_dict_word_count_cat[ int_cat ] # retrieve the word count of the category
                        for word in dict_word_count_cat :
                            if word not in dict_word_count :
                                dict_word_count[ word ] = dict_word_count_cat[ word ]
                            else :
                                dict_word_count[ word ] += dict_word_count_cat[ word ]

        # return the results
        if flag_group_is_used :
            return dict( ( l_group[ int_group ], dict_int_group_to_dict_word_count[ int_group ] ) for int_group in dict_int_group_to_dict_word_count ) # replace int_group with group
        else :
            return dict_word_count

    def visualize_word_count( 
        self,
        word_count : Dict, # a dictionary returned by 'get_word_count' function
        plot_type : Literal[ 'wordcloud', 'cloud', 'wc', 'piechart', 'pie' ] = 'wordcloud',
        l_group : Union[ None, List ] = None, # a subset of the name of the categories representing 
        kwargs_wordcloud : Dict = dict( ),
        int_num_subplots_in_a_row : int = 3, # number of subplots for each row
        int_diameter_pixel : int = 300, # diameter of the word cloud
        title : Union[ str, None ] = None, # title of the plot
        int_max_num_characters_in_a_line : int = 30, # the limit of the number of characters that can be written in a single line. if the name of the category exceed this number, a new line character will be added.
        float_min_frequency_of_a_word : float = 0.025, # the minimum frequency of a word to be included in the pie chart
    ) :
        """ # 2023-05-12 01:12:03 
        visualize word clouds

        word_count : Dict, # a dictionary returned by 'get_word_count' function
        plot_type : Literal[ 'wordcloud', 'cloud', 'wc', 'piechart', 'pie' ] = 'wordcloud',
        l_group : Union[ None, List ] = None, # a subset of the name of the categories representing 
        kwargs_wordcloud : Dict = dict( ),
        int_num_subplots_in_a_row : int = 3, # number of subplots for each row
        int_diameter_pixel : int = 500, # diameter of the word cloud
        title : Union[ str, None ] = 'Word Cloud', # title of the plot
        """
        flag_draw_word_cloud = plot_type in { 'wordcloud', 'cloud', 'wc' } # retrieve a flag for drawing word cloud
        # import packages and settings
        if flag_draw_word_cloud :
            import matplotlib.pyplot as plt
            from wordcloud import WordCloud

            # create mask for drawing word cloud
            x, y = np.ogrid[:int_diameter_pixel, :int_diameter_pixel]
            int_radius = int( int_diameter_pixel / 2 )
            mask = (x - int_radius ) ** 2 + (y - int_radius ) ** 2 > int( int_radius * 0.95 ) ** 2
            mask = 255 * mask.astype(int)

            kwargs_wordcloud_default = { 'prefer_horizontal' : 1, 'repeat' : False, 'relative_scaling' : 0.5, 'background_color' : "white", 'mode' : 'RGB', 'mask' : mask } # default settings
            kwargs_wordcloud_default.update( kwargs_wordcloud ) # update kwargs
            if 'colormap' in kwargs_wordcloud_default : # remove the 'colormap' keyword
                kwargs_wordcloud_default.pop( 'colormap' )

            # define list of color map to use
            l_cmap = [ 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'copper', 'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'coolwarm', 'twilight', 'twilight_shifted', 'hsv', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gnuplot', 'flag', 'prism' ]
            int_num_cmap = len( l_cmap )
        else :
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots

        if len( word_count ) == 0 :
            return
        if isinstance( word_count[ list( word_count )[ 0 ] ], dict ) : # if word count dictionary for each group was given
            word_count = dict( ( k, word_count[ k ] ) for k in word_count if len( word_count[ k ] ) > 0 ) # exclude empty group
            if l_group is not None : # if 'l_group' has been given, only use the groups in 'l_group'
                set_group = set( l_group )
                word_count = dict( ( k, word_count[ k ] ) for k in word_count if k in set_group )
            int_num_group = len( word_count )
            if int_num_group == 0 :
                return

            # initialize the plot
            int_num_subplots_in_a_col = int( np.ceil( int_num_group / int_num_subplots_in_a_row ) ) # get 'int_num_subplots_in_a_col'
            l_group_to_plot = list( word_count ) if l_group is None else list( group for group in l_group if group in word_count ) # retrieve the list of group for plotting (preserve the order in 'l_group' if the list was given.)
            if flag_draw_word_cloud :
                fig, axes = plt.subplots( int_num_subplots_in_a_col, int_num_subplots_in_a_row, figsize = ( int_num_subplots_in_a_row * 3.5, int_num_subplots_in_a_col * 5 ) ) # automatically set a figsize according to the grid
            else :
                fig = make_subplots( int_num_subplots_in_a_col, int_num_subplots_in_a_row, specs=[ [ {'type':'domain'} ] * ( int_num_subplots_in_a_row ) ] * int_num_subplots_in_a_col, subplot_titles = list( STR.Insert_characters_every_n_characters( e, int_max_num_characters_in_a_line, '<br>' ) for e in l_group_to_plot ) )

            # iterate each group to make a plot
            index_group = 0 
            for i in range( int_num_subplots_in_a_col ) :
                for j in range( int_num_subplots_in_a_row ) :
                    if flag_draw_word_cloud :
                        ax = axes[i][j] # retrieve the ax
                        if index_group == int_num_group : # if all groups were visualized, fill empty subplots
                            ax.axis("off")
                        else :
                            group = l_group_to_plot[ index_group ] # retrieve group
                            ax.set_title( STR.Insert_characters_every_n_characters( group, int_max_num_characters_in_a_line, '\n' ), fontsize = 10 ) # use group name as a title
                            ax.axis("off")
                            wc = WordCloud( colormap = kwargs_wordcloud[ 'colormap' ] if 'colormap' in kwargs_wordcloud else l_cmap[ int( np.random.random( ) * int_num_cmap ) ], ** kwargs_wordcloud_default )
                            wc.generate_from_frequencies( word_count[ group ] )
                            ax.imshow(wc, interpolation="bilinear")
                            index_group += 1 # update the index

                    else :
                        if index_group != int_num_group : # if all groups were visualized, fill empty subplots
                            group = l_group_to_plot[ index_group ] # retrieve group

                            s = pd.Series( word_count[ group ] ).sort_values( ascending = False )
                            s = s[ s / s.sum( ) > float_min_frequency_of_a_word ] # exclude words with the minimum frequency
                            fig.add_trace(go.Pie(labels=s.index.values, values=s.values, textinfo='label', name=STR.Insert_characters_every_n_characters( group, int_max_num_characters_in_a_line, '<br>' )), i + 1, j + 1 ) # , scalegroup='one'
                            index_group += 1 # update the index

            # set the figure size
            if not flag_draw_word_cloud :
                fig.update_layout( width = int_num_subplots_in_a_row * 350, height = int_num_subplots_in_a_col * 500, autosize = False )

            # set the title
            if title is not None : 
                if flag_draw_word_cloud :
                    fig.suptitle( STR.Insert_characters_every_n_characters( title, int_max_num_characters_in_a_line, '\n' ) )
                else :
                    fig.update_layout(title_text = STR.Insert_characters_every_n_characters( title, int_max_num_characters_in_a_line, '<br>' ) )
        else : # if a word count of all entries as one group has been given.
            if flag_draw_word_cloud :
                fig, ax = plt.subplots( 1, 1, figsize = ( 3.5, 5 ) )

                ax.axis("off")
                wc = WordCloud( colormap = kwargs_wordcloud[ 'colormap' ] if 'colormap' in kwargs_wordcloud else l_cmap[ int( np.random.random( ) * int_num_cmap ) ], ** kwargs_wordcloud_default )
                wc.generate_from_frequencies( word_count )
                ax.imshow(wc, interpolation="bilinear")
            else :
                s = pd.Series( word_count ).sort_values( ascending = False )
                s = s[ s / s.sum( ) > float_min_frequency_of_a_word ] # exclude words with the minimum frequency
                fig = go.Figure(data=[go.Pie(labels=s.index.values, values=s.values, textinfo='label+percent')])

            # set the figure size
            if not flag_draw_word_cloud :
                fig.update_layout( width = 700, height = 500, autosize = False )

            # set the title
            if title is not None : 
                if flag_draw_word_cloud :
                    fig.suptitle( STR.Insert_characters_every_n_characters( title, int_max_num_characters_in_a_line, '\n' ) )
                else :
                    fig.update_layout(title_text = STR.Insert_characters_every_n_characters( title, int_max_num_characters_in_a_line, '<br>' ) )

        # show the plot
        if flag_draw_word_cloud :
            plt.show() 
        else :
            fig.show( ) 
    
    """ scarab-associated methods for analyzing RamData """

    def _classify_feature_of_scarab_output_(
        self, int_min_num_occurrence_to_identify_valid_feature_category=1000
    ):
        """# 2022-05-30 12:39:01
        classify features of count matrix from the scarab output.
        the results will be saved at '_dict_data_for_feature_classification' attribute of the current object. In order to re-run this function with a new setting, please delete the '_dict_data_for_feature_classification' attribute of the current RamData object
        """
        """
        classify scarab features based on a specific format of Scarab output
        """
        if not hasattr(
            self, "_dict_data_for_feature_classification"
        ):  # if features were not classified yet, perform classification of features
            """retrieve 'name_feature_category_simple'"""
            # retrieve set of int_feature for each simple classification labels
            dict_name_feature_category_simple_to_num_features = dict()
            for int_feature, name_feature in enumerate(self.adata.var.index.values):
                name_feature_category_simple = name_feature.split("|", 1)[0]
                if (
                    name_feature_category_simple
                    not in dict_name_feature_category_simple_to_num_features
                ):
                    dict_name_feature_category_simple_to_num_features[
                        name_feature_category_simple
                    ] = 0
                dict_name_feature_category_simple_to_num_features[
                    name_feature_category_simple
                ] += 1  # count current int_feature according to the identified name_feature_category_simple

            # drop name_feature with the number of features smaller than the given threshold
            for name_feature_category_simple in list(
                dict_name_feature_category_simple_to_num_features
            ):
                if (
                    dict_name_feature_category_simple_to_num_features[
                        name_feature_category_simple
                    ]
                    < int_min_num_occurrence_to_identify_valid_feature_category
                ):
                    dict_name_feature_category_simple_to_num_features.pop(
                        name_feature_category_simple
                    )

            # l_name_feaure_category_simple = [ '' ] + list( dict_name_feature_category_simple_to_num_features )
            # dict_name_feature_category_simple_to_int = dict( ( e, i ) for i, e in enumerate( l_name_feaure_category_simple ) )

            """ retrieve 'name_feature_category_detailed' """
            l_name_feaure_category_detailed = (
                []
            )  # initialize 'l_name_feaure_category_simple'
            dict_name_feaure_category_detailed_to_int = (
                dict()
            )  # initialize 'dict_name_feaure_category_detailed_to_int'
            arr_int_feature_category_detailed = np.zeros(
                self._int_num_features, dtype=np.int16
            )  # retrieve mapping from int_feature to int_feature_category
            for int_feature, name_feature in enumerate(self.adata.var.index.values):
                l_entry = list(
                    e.split("=", 1)[0] for e in name_feature.split("|")
                )  # retrieve entry composing the name_feature
                if (
                    l_entry[0] not in dict_name_feature_category_simple_to_num_features
                ):  # remove the first entry for feature with invalid name_feature_category_simple (features of each gene)
                    l_entry = l_entry[1:]
                str_category_feature_detailed = "___".join(l_entry).replace(
                    "mode", "atac_mode"
                )  # compose str_category_feature_detailed

                if (
                    str_category_feature_detailed
                    not in dict_name_feaure_category_detailed_to_int
                ):  # append new 'name_feaure_category_detailed' as it is detected
                    dict_name_feaure_category_detailed_to_int[
                        str_category_feature_detailed
                    ] = len(l_name_feaure_category_detailed)
                    l_name_feaure_category_detailed.append(
                        str_category_feature_detailed
                    )
                arr_int_feature_category_detailed[
                    int_feature
                ] = dict_name_feaure_category_detailed_to_int[
                    str_category_feature_detailed
                ]

            # accessory function
            def get_int_feature_category_detailed(int_feature):
                return arr_int_feature_category_detailed[int_feature]

            vectorized_get_int_feature_category_detailed = np.vectorize(
                get_int_feature_category_detailed
            )  # vectorize the function to increase efficiency

            # build a mask of features of atac mode
            l_mask_feature_category_of_atac_mode = Search_list_of_strings_Return_mask(
                l_name_feaure_category_detailed, "atac_mode"
            )
            ba_mask_feature_of_atac_mode = bitarray(
                len(arr_int_feature_category_detailed)
            )
            ba_mask_feature_of_atac_mode.setall(0)
            for int_feature, int_feature_category in enumerate(
                arr_int_feature_category_detailed
            ):
                if l_mask_feature_category_of_atac_mode[int_feature_category]:
                    ba_mask_feature_of_atac_mode[int_feature] = 1

            # save result and settings to the current object
            self._dict_data_for_feature_classification = {
                "int_min_num_occurrence_to_identify_valid_feature_category": int_min_num_occurrence_to_identify_valid_feature_category,
                "l_name_feaure_category_detailed": l_name_feaure_category_detailed,
                "dict_name_feaure_category_detailed_to_int": dict_name_feaure_category_detailed_to_int,
                "arr_int_feature_category_detailed": arr_int_feature_category_detailed,
                "get_int_feature_category_detailed": get_int_feature_category_detailed,
                "vectorized_get_int_feature_category_detailed": vectorized_get_int_feature_category_detailed,
                "l_mask_feature_category_of_atac_mode": l_mask_feature_category_of_atac_mode,
                "ba_mask_feature_of_atac_mode": ba_mask_feature_of_atac_mode,
                "dict_name_feature_category_simple_to_num_features": dict_name_feature_category_simple_to_num_features,
            }  # set the object as an attribute of the object so that the object is available in the child processes consistently

    def _further_summarize_scarab_output_for_filtering_(
        self, name_layer="raw", name_adata="main", flag_show_graph=True
    ):
        """# 2022-06-06 01:01:47
        (1) calculate the total count in gex mode
        (2) calculate_proportion_of_promoter_in_atac_mode
        assumming Scarab output and the output of 'sum_scarab_feature_category', calculate the ratio of counts of promoter features to the total counts in atac mode.

        'name_layer' : name of the data from which scarab_feature_category summary was generated. by default, 'raw'
        'name_adata' : name of the AnnData of the current RamData object. by default, 'main'
        """
        df = self.ad[name_adata].obs  # retrieve data of the given AnnData

        # calculate gex metrics
        df[f"{name_layer}_sum_for_gex_mode"] = df[
            bk.Search_list_of_strings_with_multiple_query(
                df.columns, f"{name_layer}_sum__", "-atac_mode"
            )
        ].sum(
            axis=1
        )  # calcualte sum for gex mode outputs

        # calcualte atac metrics
        if (
            f"{name_layer}_sum___category_detailed___atac_mode" in df.columns.values
        ):  # check whether the ATAC mode has been used in the scarab output
            df[f"{name_layer}_sum_for_atac_mode"] = df[
                bk.Search_list_of_strings_with_multiple_query(
                    df.columns, f"{name_layer}_sum__", "atac_mode"
                )
            ].sum(
                axis=1
            )  # calcualte sum for atac mode outputs
            df[f"{name_layer}_sum_for_promoter_atac_mode"] = df[
                list(
                    bk.Search_list_of_strings_with_multiple_query(
                        df.columns,
                        f"{name_layer}_sum___category_detailed___promoter",
                        "atac_mode",
                    )
                )
            ].sum(axis=1)
            df[f"{name_layer}_proportion_of_promoter_in_atac_mode"] = (
                df[f"{name_layer}_sum_for_promoter_atac_mode"]
                / df[f"{name_layer}_sum_for_atac_mode"]
            )  # calculate the proportion of reads in promoter
            df[f"{name_layer}_proportion_of_promoter_and_gene_body_in_atac_mode"] = (
                df[f"{name_layer}_sum_for_promoter_atac_mode"]
                + df[f"{name_layer}_sum___category_detailed___atac_mode"]
            ) / df[
                f"{name_layer}_sum_for_atac_mode"
            ]  # calculate the proportion of reads in promoter

            # show graphs
            if flag_show_graph:
                MPL_Scatter_Align_Two_Series(
                    df[f"{name_layer}_sum_for_atac_mode"],
                    df[f"{name_layer}_sum_for_gex_mode"],
                    x_scale="log",
                    y_scale="log",
                    alpha=0.005,
                )
                MPL_Scatter_Align_Two_Series(
                    df[f"{name_layer}_sum_for_atac_mode"],
                    df[f"{name_layer}_proportion_of_promoter_in_atac_mode"],
                    x_scale="log",
                    alpha=0.01,
                )

        self.ad[name_adata].obs = df  # save the result

    def _filter_cell_scarab_output_(
        self,
        path_folder_ramdata_output,
        name_layer="raw",
        name_adata="main",
        int_min_sum_for_atac_mode=1500,
        float_min_proportion_of_promoter_in_atac_mode=0.22,
        int_min_sum_for_gex_mode=250,
    ):
        """# 2022-06-03 15:25:02
        filter cells from scarab output

        'path_folder_ramdata_output' : output directory
        """
        df = self.ad[name_adata].obs  # retrieve data of the given AnnData

        # retrieve barcodes for filtering
        set_str_barcode = df[
            (df[f"{name_layer}_sum_for_atac_mode"] >= int_min_sum_for_atac_mode)
            & (
                df[f"{name_layer}_proportion_of_promoter_in_atac_mode"]
                >= float_min_proportion_of_promoter_in_atac_mode
            )
            & (df[f"{name_layer}_sum_for_gex_mode"] >= int_min_sum_for_gex_mode)
        ].index.values
        # subset the current RamData for valid cells
        self.subset(path_folder_ramdata_output, set_str_barcode=set_str_barcode)
        if self.verbose:
            logger.info(
                f"cell filtering completed for {len( set_str_barcode )} cells. A filtered RamData was exported at {path_folder_ramdata_output}"
            )
