import logging

import pyspark

from distributed_pe_processor.src.transform import binary_metadata_reader


def transform_files_to_metadata(binary_files_rdd: pyspark.rdd.RDD, logger = logging.getLogger(__name__)):
    """
    Extracts and returns metadata from binary files using an RDD map transformation.\n\n

    Parameters:\n
    - binary_files_rdd : RDD\n
        An RDD containing binary file data.\n

    Returns:\n
    - metadata_rdd : RDD \n
        An RDD of extracted metadata from the binary files.
    """
    logger.info("Start to extract and returns metadata from binary files")
    metadata_rdd = binary_files_rdd.map(binary_metadata_reader.get_metadata)
    logger.info("Received metadata from binary files")
    return metadata_rdd
