from __future__ import annotations

import codecs
import os
from copy import copy, deepcopy
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import attrs

from .. import helpers, settings
from ..dialect import Dialect
from ..exception import FrictionlessException
from ..fields import AnyField
from ..metadata import Metadata
from ..platform import platform
from ..schema import Field, Schema

if TYPE_CHECKING:
    from .. import types
    from ..resource import Resource


@attrs.define(kw_only=True, repr=False)
class Detector:
    """Detector representation.

    This main purpose of this class is to set the parameters to define
    how different aspects of metadata are detected.

    """

    buffer_size: int = settings.DEFAULT_BUFFER_SIZE
    """
    The amount of bytes to be extracted as a buffer. It defaults to 10000.
    The buffer_size can be increased to improve the inference accuracy to
    detect file encoding.
    """

    sample_size: int = settings.DEFAULT_SAMPLE_SIZE
    """
    The amount of rows to be extracted as a sample for dialect/schema inferring.
    It defaults to 100. The sample_size can be increased to improve the inference
    accuracy.
    """

    encoding_function: Optional[types.IEncodingFunction] = None
    """
    A custom encoding function for the file.
    """

    encoding_confidence: float = settings.DEFAULT_ENCODING_CONFIDENCE
    """
    Confidence value for encoding function.
    """

    field_type: Optional[str] = None
    """
    Enforce all the inferred types to be this type.
    For more information, please check "Describing  Data" guide.
    """

    field_names: Optional[List[str]] = None
    """
    Enforce all the inferred fields to have provided names.
    For more information, please check "Describing  Data" guide.
    """

    field_confidence: float = settings.DEFAULT_FIELD_CONFIDENCE
    """
    A number from 0 to 1 setting the infer confidence.
    If  1 the data is guaranteed to be valid against the inferred schema.
    For more information, please check "Describing  Data" guide.
    It defaults to 0.9
    """

    field_float_numbers: bool = settings.DEFAULT_FLOAT_NUMBERS
    """
    Flag to indicate desired number type.
    By default numbers will be `Decimal`; if `True` - `float`.
    For more information, please check "Describing  Data" guide.
    It defaults to `False`
    """

    field_missing_values: List[str] = attrs.field(
        factory=settings.DEFAULT_MISSING_VALUES.copy,
    )
    """
    String to be considered as missing values.
    For more information, please check "Describing  Data" guide.
    It defaults to `['']`
    """

    field_true_values: List[str] = attrs.field(
        factory=settings.DEFAULT_TRUE_VALUES.copy,
    )
    """
    String to be considered as true values.
    For more information, please check "Describing  Data" guide.
    It defaults to `["true", "True", "TRUE", "1"]`
    """

    field_false_values: List[str] = attrs.field(
        factory=settings.DEFAULT_FALSE_VALUES.copy,
    )
    """
    String to be considered as false values.
    For more information, please check "Describing  Data" guide.
    It defaults to `["false", "False", "FALSE", "0"]`
    """

    schema_sync: bool = False
    """
    Whether to sync the schema.
    If it sets to `True` the provided schema will be mapped to
    the inferred schema. It means that, for example, you can
    provide a subset of fields to be applied on top of the inferred
    fields or the provided schema can have different order of fields.
    """

    schema_patch: Optional[Dict[str, Any]] = None
    """
    A dictionary to be used as an inferred schema patch.
    The form of this dictionary should follow the Schema descriptor form
    except for the `fields` property which should be a mapping with the
    key named after a field name and the values being a field patch.
    For more information, please check "Extracting Data" guide.
    """

    # Metadta

    # TODO: remove static method?
    @staticmethod
    def detect_metadata_type(
        source: Any, *, format: Optional[str] = None
    ) -> Optional[str]:
        """Return an descriptor type as 'resource' or 'package'"""
        pass

    # Resource

    def detect_resource(self, resource: Resource) -> None:
        """Detects path details"""
        pass

    # Encoding

    def detect_encoding(
        self, buffer: types.IBuffer, *, encoding: Optional[str] = None
    ) -> str:
        """Detect encoding from buffer

        Parameters:
            buffer (byte): byte buffer

        Returns:
            str: encoding
        """
        pass

    # Dialect

    def detect_dialect(
        self,
        sample: types.ISample,
        *,
        dialect: Optional[Dialect] = None,
    ) -> Dialect:
        """Detect dialect from sample

        Parameters:
            sample (any[][]): data sample
            dialect? (Dialect): file dialect

        Returns:
            Dialect: dialect
        """
        pass

    # Schema

    # TODO: detect fields without type
    def detect_schema(
        self,
        fragment: types.IFragment,
        *,
        labels: Optional[List[str]] = None,
        schema: Optional[Schema] = None,
        field_candidates: List[Dict[str, Any]] = settings.DEFAULT_FIELD_CANDIDATES,
        **options: Any,
    ) -> Schema:
        """Detect schema from fragment

        Parameters:
            fragment (any[][]): data fragment
            labels? (str[]): data labels
            schema? (Schema): data schema

        Returns:
            Schema: schema
        """
        pass

    @staticmethod
    def mapped_schema_fields_names(
        fields: List[Field], case_sensitive: bool
    ) -> Dict[str, Field]:
        """Create a dictionnary to map field names with schema fields"""
        pass

    @staticmethod
    def rearrange_schema_fields_given_labels(
        fields_mapping: Dict[str, Field],
        schema: Schema,
        labels: List[str],
    ):
        """Rearrange fields according to the order of labels. All fields
        missing from labels are dropped"""
        pass

    def add_missing_required_labels_to_schema_fields(
        self,
        fields_mapping: Dict[str, Field],
        schema: Schema,
        labels: List[str],
        case_sensitive: bool,
    ):
        """This method aims to add missing required labels and
        primary key field not in labels to schema fields.
        """
        pass

    @staticmethod
    def field_is_required(
        field: Field,
        schema: Schema,
        case_sensitive: bool,
    ) -> bool:
        pass
