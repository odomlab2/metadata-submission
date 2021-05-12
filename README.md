# Metadata template

This repository provides a version-controlled template for metadata tracking and submission for the Odomlab2.0.

## Changelog

### 2021-05-12 - Version 2021-05.1

#### Changes

  - New fields:
     - `GENOTYPE` - needed for ArrayExpress /ENA submission, typically this is *wild type*, if not working with GMO
     - `TISSUE` - **important** if your `SAMPLE_TYPE` is not indicating the tissue, fill this field
     - `IMAGING_DATASET_ID` - ID/Label to reference imaging dataset e.g. for Spatial Transcriptomics
  - Removed redundant fields:
     - `BARCODE_I7 `
     - `BARCODE_I5`
     - use `BARCODE_I5_SEQ` and `BARCODE_I7_SEQ` instead
  - Please note that **CAST/Ej is not a species**. For `SPECIES` enter *Mus musculus* and specify the `STRAIN` **CAST/Ej**
  - Website to get info and spreadsheets: https://odomlab2.github.io/metadata-submission/
  - Columns may be sorted according to category, rather than by point-of-use 


### 2020-11-05

Added fields to Chip-Seq: 

 - ANTIBODY
 - ANTIBODY_LOT_NUMBERwq
 - ANTIBODY_TARGET
  


### 2020-10-27

#### Major Changes
Most importantly, I added two fields:
  - INDIVIDUAL_REF_ID
  - INDIVIDUAL_REF_DB

The following fields were renamed
  - LIBRARY_PREP_KIT -> LIB_PREP_KIT
  - SAMPLE_ID -> SAMPLE_NAME_GPCF
  - BIOMATERIAL_ID -> SAMPLE_TYPE


**How to use:**

The purpose of these is to provide a clear reference point to the
animals used. Thus, at the DKFZ, the INDIVIDUAL_REF_ID is the
ANIMAL_NUMBER from the MOVI database or the spreadsheet-dump located at

"T:/Animals/Animal numbers MOVI "

In this case INDIVIDUAL_REF_DB would be set to "MOVI"

For CRUK-originated samples, the animal numbers (column: "MOUSE ID" are
listed in the following spreadsheet:

T:/FREEZER -80/Freezer 2- Cambridge samples/Cambridge sample inventory
lists/190307_harvested_tissue_mouse2.xlsx

In this case INDIVIDUAL_REF_DB would be set to "ODOM_TISSUE_DB".


The field "LIB_PREP_KIT" is used by OTP to select adapter sequences for trimming of RNAseq reads.
Please check in your previous submission, if the library preparation kit that are using is registered in OTP (odcf-service@dkfz.de) or tell the ODCF
which kit you have used and which adapter it contains.

#### Minor changes
 -  Modified description banners in the bottom. It should be more clear now, that *all* fields are mandatory to fill
out, not only those for ILSE.


## Versioning

This repository used calendar-versioning (https://calver.org/) according to the following scheme:

`YY.0M-minor`

Accordingly, the first version released in October, 2020 is tagged: *20.10-1*
