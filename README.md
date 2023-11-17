![scelephant-logo](https://raw.githubusercontent.com/ahs2202/scelephant/master/doc/img/scelephant_logo.png)

# SC-Elephant (Single-Cell Extremely Large Data Analysis Platform)

[![PyPI version](https://badge.fury.io/py/scelephant.svg)](https://badge.fury.io/py/scelephant)

`SC-Elephant` utilizes `RamData`, a novel single-cell data storage format, to support a wide range of single-cell bioinformatics applications in a highly scalable manner, while providing a convenient interface to export any subset of the single-cell data in `SCANPY`'s `AnnData` format, enabling efficient downstream analysis the cells of interest. The analysis result can then be made available to other researchers by updating the original `RamData`, which can be stored in cloud storage like `AWS` (or any AWS-like object storage).



`SC-Elephant` and `RamData` enable real-time sharing of extremely large single-cell data using a browser-based analysis platform as it is being modified on the cloud by multiple other researchers, convenient integration of a local single-cell dataset with multiple large remote datasets (`RamData` objects uploaded by other researchers), and remote (private) collaboration on an extremely large-scale single-cell genomics dataset. 



Tutorials can be found at `doc/jn/`

[Tutorials) PBMC3k processing and analysis using SC-Elephant](https://scelephant-free.s3.amazonaws.com/doc/SC-Elephant_PBMC3k_processing_and_analysis_tutorials.html)

[Tutorials) Alignment of PBMC3k to the ELDB (320,000 subset) and cell type prediction using SC-Elephant](https://scelephant-free.s3.amazonaws.com/doc/SC-Elephant_PBMC3k_alignment_to_the_ELDB_subset_320k_tutorials.html)



Briefly, a <tt>RamData</tt> object is composed of two <b><tt>RamDataAxis</tt></b> (<b>Axis</b>) objects and multiple <b><tt>RamDataLayer</tt></b> (<b>Layer</b>) objects.

![ramdata_struc](https://raw.githubusercontent.com/ahs2202/scelephant/master/doc/img/ramdata_struc.png)



The two RamDataAxis objects, <b>'Barcode'</b> and <b>'Feature'</b> objects, use <b><tt>'filter'</tt></b> to select cells (barcodes) and genes (features) before retrieving data from the <tt>RamData</tt> object, respectively.

![ramdata_struc](https://raw.githubusercontent.com/ahs2202/scelephant/master/doc/img/ramtx_sparse_matrix.png)

`RamData` employs `RAMtx` (Random-accessible matrix) objects to store count matrix in sparse or dense formats.



For a demonstration of the use of `RamData` object on a web browser, please visit http://scelephant.org/

![scelephant-js-example](https://raw.githubusercontent.com/ahs2202/scelephant/master/doc/img/scelephant_js_example.png)
