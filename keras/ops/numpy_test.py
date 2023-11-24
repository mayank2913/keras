import contextlib
import itertools

import numpy as np
import pytest
from absl.testing import parameterized
from tensorflow.python.ops.numpy_ops import np_config

from keras import backend
from keras import testing
from keras.backend.common import standardize_dtype
from keras.backend.common.keras_tensor import KerasTensor
from keras.backend.common.variables import ALLOWED_DTYPES
from keras.ops import numpy as knp
from keras.testing.test_utils import named_product

# TODO: remove reliance on this (or alternatively, turn it on by default).
np_config.enable_numpy_behavior()


class NumpyTwoInputOpsDynamicShapeTest(testing.TestCase):
    def test_add(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.add(x, y).shape, (2, 3))

    def test_subtract(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.subtract(x, y).shape, (2, 3))

    def test_multiply(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.multiply(x, y).shape, (2, 3))

    def test_matmul(self):
        x = KerasTensor((None, 3, 4))
        y = KerasTensor((3, None, 4, 5))
        self.assertEqual(knp.matmul(x, y).shape, (3, None, 3, 5))

    def test_power(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.power(x, y).shape, (2, 3))

    def test_divide(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.divide(x, y).shape, (2, 3))

    def test_true_divide(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.true_divide(x, y).shape, (2, 3))

    def test_append(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.append(x, y).shape, (None,))

    def test_arctan2(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.arctan2(x, y).shape, (2, 3))

    def test_cross(self):
        x1 = KerasTensor((2, 3, 3))
        x2 = KerasTensor((1, 3, 2))
        y = KerasTensor((None, 1, 2))
        self.assertEqual(knp.cross(x1, y).shape, (2, 3, 3))
        self.assertEqual(knp.cross(x2, y).shape, (None, 3))

    def test_einsum(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((3, 4))
        self.assertEqual(knp.einsum("ij,jk->ik", x, y).shape, (None, 4))
        self.assertEqual(knp.einsum("ij,jk->ikj", x, y).shape, (None, 4, 3))
        self.assertEqual(knp.einsum("ii", x).shape, ())
        self.assertEqual(knp.einsum(",ij", 5, x).shape, (None, 3))

        x = KerasTensor((None, 3, 4))
        y = KerasTensor((None, 4, 5))
        z = KerasTensor((1, 1, 1, 9))
        self.assertEqual(knp.einsum("ijk,jkl->li", x, y).shape, (5, None))
        self.assertEqual(knp.einsum("ijk,jkl->lij", x, y).shape, (5, None, 3))
        self.assertEqual(
            knp.einsum("...,...j->...j", x, y).shape, (None, 3, 4, 5)
        )
        self.assertEqual(
            knp.einsum("i...,...j->i...j", x, y).shape, (None, 3, 4, 5)
        )
        self.assertEqual(knp.einsum("i...,...j", x, y).shape, (3, 4, None, 5))
        self.assertEqual(
            knp.einsum("i...,...j,...k", x, y, z).shape, (1, 3, 4, None, 5, 9)
        )
        self.assertEqual(
            knp.einsum("mij,ijk,...", x, y, z).shape, (1, 1, 1, 9, 5, None)
        )

        with self.assertRaises(ValueError):
            x = KerasTensor((None, 3))
            y = KerasTensor((3, 4))
            knp.einsum("ijk,jk->ik", x, y)

    def test_full_like(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.full_like(x, KerasTensor((1, 3))).shape, (None, 3))

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.full_like(x, 2).shape, (None, 3, 3))

    def test_greater(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.greater(x, y).shape, (2, 3))

    def test_greater_equal(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.greater_equal(x, y).shape, (2, 3))

    def test_isclose(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.isclose(x, y).shape, (2, 3))

    def test_less(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.less(x, y).shape, (2, 3))

    def test_less_equal(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.less_equal(x, y).shape, (2, 3))

    def test_linspace(self):
        start = KerasTensor((None, 3, 4))
        stop = KerasTensor((2, 3, 4))
        self.assertEqual(
            knp.linspace(start, stop, 10, axis=1).shape, (2, 10, 3, 4)
        )

        start = KerasTensor((None, 3))
        stop = 2
        self.assertEqual(
            knp.linspace(start, stop, 10, axis=1).shape, (None, 10, 3)
        )

    def test_logical_and(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.logical_and(x, y).shape, (2, 3))

    def test_logical_or(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.logical_or(x, y).shape, (2, 3))

    def test_logspace(self):
        start = KerasTensor((None, 3, 4))
        stop = KerasTensor((2, 3, 4))
        self.assertEqual(
            knp.logspace(start, stop, 10, axis=1).shape, (2, 10, 3, 4)
        )

        start = KerasTensor((None, 3))
        stop = 2
        self.assertEqual(
            knp.logspace(start, stop, 10, axis=1).shape, (None, 10, 3)
        )

    def test_maximum(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.maximum(x, y).shape, (2, 3))

    def test_minimum(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.minimum(x, y).shape, (2, 3))

    def test_mod(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.mod(x, y).shape, (2, 3))

    def test_not_equal(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.not_equal(x, y).shape, (2, 3))

    def test_outer(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.outer(x, y).shape, (None, None))

    def test_quantile(self):
        x = KerasTensor((None, 3))

        # q as scalar
        q = KerasTensor(())
        self.assertEqual(knp.quantile(x, q).shape, ())

        # q as 1D tensor
        q = KerasTensor((2,))
        self.assertEqual(knp.quantile(x, q).shape, (2,))
        self.assertEqual(knp.quantile(x, q, axis=1).shape, (2, None))
        self.assertEqual(
            knp.quantile(x, q, axis=1, keepdims=True).shape,
            (2, None, 1),
        )

    def test_take(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.take(x, 1).shape, ())
        self.assertEqual(knp.take(x, [1, 2]).shape, (2,))
        self.assertEqual(
            knp.take(x, [[1, 2], [1, 2]], axis=1).shape, (None, 2, 2)
        )

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.take(x, 1, axis=1).shape, (None, 3))
        self.assertEqual(knp.take(x, [1, 2]).shape, (2,))
        self.assertEqual(
            knp.take(x, [[1, 2], [1, 2]], axis=1).shape, (None, 2, 2, 3)
        )

        # test with negative axis
        self.assertEqual(knp.take(x, 1, axis=-2).shape, (None, 3))

        # test with multi-dimensional indices
        x = KerasTensor((None, 3, None, 5))
        indices = KerasTensor((6, 7))
        self.assertEqual(knp.take(x, indices, axis=2).shape, (None, 3, 6, 7, 5))

    def test_take_along_axis(self):
        x = KerasTensor((None, 3))
        indices = KerasTensor((1, 3))
        self.assertEqual(knp.take_along_axis(x, indices, axis=0).shape, (1, 3))
        self.assertEqual(
            knp.take_along_axis(x, indices, axis=1).shape, (None, 3)
        )

        x = KerasTensor((None, 3, 3))
        indices = KerasTensor((1, 3, None))
        self.assertEqual(
            knp.take_along_axis(x, indices, axis=1).shape, (None, 3, 3)
        )

    def test_tensordot(self):
        x = KerasTensor((None, 3, 4))
        y = KerasTensor((3, 4))
        self.assertEqual(knp.tensordot(x, y, axes=1).shape, (None, 3, 4))
        self.assertEqual(knp.tensordot(x, y, axes=[[0, 1], [1, 0]]).shape, (4,))

    def test_vdot(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((None, 3))
        self.assertEqual(knp.vdot(x, y).shape, ())

        x = KerasTensor((None, 3, 3))
        y = KerasTensor((None, 3, 3))
        self.assertEqual(knp.vdot(x, y).shape, ())

    def test_where(self):
        condition = KerasTensor((2, None, 1))
        x = KerasTensor((None, 1))
        y = KerasTensor((None, 3))
        self.assertEqual(knp.where(condition, x, y).shape, (2, None, 3))
        self.assertEqual(knp.where(condition).shape, (2, None, 1))

    def test_floordiv(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.floor_divide(x, y).shape, (2, 3))

    def test_xor(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((2, None))
        self.assertEqual(knp.logical_xor(x, y).shape, (2, 3))

    def test_shape_equal_basic_equality(self):
        x = KerasTensor((3, 4)).shape
        y = KerasTensor((3, 4)).shape
        self.assertTrue(knp.shape_equal(x, y))
        y = KerasTensor((3, 5)).shape
        self.assertFalse(knp.shape_equal(x, y))

    def test_shape_equal_allow_none(self):
        x = KerasTensor((3, 4, None)).shape
        y = KerasTensor((3, 4, 5)).shape
        self.assertTrue(knp.shape_equal(x, y, allow_none=True))
        self.assertFalse(knp.shape_equal(x, y, allow_none=False))

    def test_shape_equal_different_shape_lengths(self):
        x = KerasTensor((3, 4)).shape
        y = KerasTensor((3, 4, 5)).shape
        self.assertFalse(knp.shape_equal(x, y))

    def test_shape_equal_ignore_axes(self):
        x = KerasTensor((3, 4, 5)).shape
        y = KerasTensor((3, 6, 5)).shape
        self.assertTrue(knp.shape_equal(x, y, axis=1))
        y = KerasTensor((3, 6, 7)).shape
        self.assertTrue(knp.shape_equal(x, y, axis=(1, 2)))
        self.assertFalse(knp.shape_equal(x, y, axis=1))

    def test_shape_equal_only_none(self):
        x = KerasTensor((None, None)).shape
        y = KerasTensor((5, 6)).shape
        self.assertTrue(knp.shape_equal(x, y, allow_none=True))

    def test_shape_equal_axis_as_list(self):
        x = KerasTensor((3, 4, 5)).shape
        y = KerasTensor((3, 6, 5)).shape
        self.assertTrue(knp.shape_equal(x, y, axis=[1]))

    def test_shape_non_equal_with_negative_axis(self):
        x = KerasTensor((3, 4, 5)).shape
        y = KerasTensor((3, 4, 6)).shape
        self.assertFalse(knp.shape_equal(x, y, axis=-2))

    def test_shape_equal_with_negative_axis(self):
        x = KerasTensor((3, 4, 5)).shape
        y = KerasTensor((3, 4, 5)).shape
        self.assertTrue(knp.shape_equal(x, y, axis=-1))

    def test_shape_equal_zeros(self):
        x = KerasTensor((0, 4)).shape
        y = KerasTensor((0, 4)).shape
        self.assertTrue(knp.shape_equal(x, y))
        y = KerasTensor((0, 5)).shape
        self.assertFalse(knp.shape_equal(x, y))

    def test_broadcast_shapes_conversion_to_list(self):
        shape1 = KerasTensor((1, 2)).shape
        shape2 = KerasTensor((3, 1)).shape
        expected_output = [3, 2]
        self.assertEqual(knp.broadcast_shapes(shape1, shape2), expected_output)

    def test_broadcast_shapes_shape1_longer_than_shape2(self):
        shape1 = KerasTensor((5, 3, 2)).shape
        shape2 = KerasTensor((1, 3)).shape
        with self.assertRaisesRegex(ValueError, "Cannot broadcast shape"):
            knp.broadcast_shapes(shape1, shape2)

    def test_broadcast_shapes_shape2_longer_than_shape1(self):
        shape1 = KerasTensor((5, 3)).shape
        shape2 = KerasTensor((2, 5, 3)).shape
        expected_output = [2, 5, 3]
        self.assertEqual(knp.broadcast_shapes(shape1, shape2), expected_output)

    def test_broadcast_shapes_broadcasting_shape1_is_1(self):
        shape1 = KerasTensor((1, 3)).shape
        shape2 = KerasTensor((5, 1)).shape
        expected_output = [5, 3]
        self.assertEqual(knp.broadcast_shapes(shape1, shape2), expected_output)

    def test_broadcast_shapes_broadcasting_shape1_is_none(self):
        shape1 = KerasTensor((None, 3)).shape
        shape2 = KerasTensor((5, 1)).shape
        expected_output = [5, 3]
        self.assertEqual(knp.broadcast_shapes(shape1, shape2), expected_output)

        shape1 = KerasTensor((None, 3)).shape
        shape2 = KerasTensor((5, 3)).shape
        expected_output = [5, 3]
        self.assertEqual(knp.broadcast_shapes(shape1, shape2), expected_output)

    def test_broadcast_shapes_broadcasting_shape2_conditions(self):
        shape1 = KerasTensor((5, 3, 2)).shape
        shape2 = KerasTensor((1, 3, 2)).shape
        expected_output = [5, 3, 2]
        self.assertEqual(knp.broadcast_shapes(shape1, shape2), expected_output)

        shape1 = KerasTensor((5, 3, 2)).shape
        shape2 = KerasTensor((1, None, 2)).shape
        expected_output = [5, 3, 2]
        self.assertEqual(knp.broadcast_shapes(shape1, shape2), expected_output)


class NumpyTwoInputOpsStaticShapeTest(testing.TestCase):
    def test_add(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.add(x, y).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.add(x, y)

    def test_subtract(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.subtract(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.subtract(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.subtract(x, y)

    def test_multiply(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.multiply(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.multiply(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.multiply(x, y)

    def test_matmul(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((3, 2))
        self.assertEqual(knp.matmul(x, y).shape, (2, 2))

        with self.assertRaises(ValueError):
            x = KerasTensor((3, 4))
            y = KerasTensor((2, 3, 4))
            knp.matmul(x, y)

    def test_matmul_sparse(self):
        x = KerasTensor((2, 3), sparse=True)
        y = KerasTensor((3, 2))
        result = knp.matmul(x, y)
        self.assertEqual(result.shape, (2, 2))

        x = KerasTensor((2, 3))
        y = KerasTensor((3, 2), sparse=True)
        result = knp.matmul(x, y)
        self.assertEqual(result.shape, (2, 2))

        x = KerasTensor((2, 3), sparse=True)
        y = KerasTensor((3, 2), sparse=True)
        result = knp.matmul(x, y)
        self.assertEqual(result.shape, (2, 2))
        self.assertTrue(result.sparse)

    def test_power(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.power(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.power(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.power(x, y)

    def test_divide(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.divide(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.divide(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.divide(x, y)

    def test_true_divide(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.true_divide(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.true_divide(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.true_divide(x, y)

    def test_append(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.append(x, y).shape, (12,))

        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.append(x, y, axis=0).shape, (4, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.append(x, y, axis=2)

    def test_arctan2(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.arctan2(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.arctan2(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.arctan2(x, y)

    def test_cross(self):
        x1 = KerasTensor((2, 3, 3))
        x2 = KerasTensor((1, 3, 2))
        y1 = KerasTensor((2, 3, 3))
        y2 = KerasTensor((2, 3, 2))
        self.assertEqual(knp.cross(x1, y1).shape, (2, 3, 3))
        self.assertEqual(knp.cross(x2, y2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.cross(x, y)

        with self.assertRaises(ValueError):
            x = KerasTensor((4, 3, 3))
            y = KerasTensor((2, 3, 3))
            knp.cross(x, y)

    def test_einsum(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((3, 4))
        self.assertEqual(knp.einsum("ij,jk->ik", x, y).shape, (2, 4))
        self.assertEqual(knp.einsum("ij,jk->ikj", x, y).shape, (2, 4, 3))
        self.assertEqual(knp.einsum("ii", x).shape, ())
        self.assertEqual(knp.einsum(",ij", 5, x).shape, (2, 3))

        x = KerasTensor((2, 3, 4))
        y = KerasTensor((3, 4, 5))
        z = KerasTensor((1, 1, 1, 9))
        self.assertEqual(knp.einsum("ijk,jkl->li", x, y).shape, (5, 2))
        self.assertEqual(knp.einsum("ijk,jkl->lij", x, y).shape, (5, 2, 3))
        self.assertEqual(knp.einsum("...,...j->...j", x, y).shape, (2, 3, 4, 5))
        self.assertEqual(
            knp.einsum("i...,...j->i...j", x, y).shape, (2, 3, 4, 5)
        )
        self.assertEqual(knp.einsum("i...,...j", x, y).shape, (3, 4, 2, 5))
        self.assertEqual(knp.einsum("i...,...j", x, y).shape, (3, 4, 2, 5))
        self.assertEqual(
            knp.einsum("i...,...j,...k", x, y, z).shape, (1, 3, 4, 2, 5, 9)
        )
        self.assertEqual(
            knp.einsum("mij,ijk,...", x, y, z).shape, (1, 1, 1, 9, 5, 2)
        )

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((3, 4))
            knp.einsum("ijk,jk->ik", x, y)

    def test_full_like(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.full_like(x, 2).shape, (2, 3))

    def test_greater(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.greater(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.greater(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.greater(x, y)

    def test_greater_equal(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.greater_equal(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.greater_equal(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.greater_equal(x, y)

    def test_isclose(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.isclose(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.isclose(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.isclose(x, y)

    def test_less(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.less(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.less(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.less(x, y)

    def test_less_equal(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.less_equal(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.less_equal(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.less_equal(x, y)

    def test_linspace(self):
        start = KerasTensor((2, 3, 4))
        stop = KerasTensor((2, 3, 4))
        self.assertEqual(knp.linspace(start, stop, 10).shape, (10, 2, 3, 4))

        with self.assertRaises(ValueError):
            start = KerasTensor((2, 3))
            stop = KerasTensor((2, 3, 4))
            knp.linspace(start, stop)

    def test_logical_and(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.logical_and(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.logical_and(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.logical_and(x, y)

    def test_logical_or(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.logical_or(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.logical_or(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.logical_or(x, y)

    def test_logspace(self):
        start = KerasTensor((2, 3, 4))
        stop = KerasTensor((2, 3, 4))
        self.assertEqual(knp.logspace(start, stop, 10).shape, (10, 2, 3, 4))

        with self.assertRaises(ValueError):
            start = KerasTensor((2, 3))
            stop = KerasTensor((2, 3, 4))
            knp.logspace(start, stop)

    def test_maximum(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.maximum(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.maximum(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.maximum(x, y)

    def test_minimum(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.minimum(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.minimum(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.minimum(x, y)

    def test_mod(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.mod(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.mod(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.mod(x, y)

    def test_not_equal(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.not_equal(x, y).shape, (2, 3))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.not_equal(x, 2).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.not_equal(x, y)

    def test_outer(self):
        x = KerasTensor((3,))
        y = KerasTensor((4,))
        self.assertEqual(knp.outer(x, y).shape, (3, 4))

        x = KerasTensor((2, 3))
        y = KerasTensor((4, 5))
        self.assertEqual(knp.outer(x, y).shape, (6, 20))

        x = KerasTensor((2, 3))
        self.assertEqual(knp.outer(x, 2).shape, (6, 1))

    def test_quantile(self):
        x = KerasTensor((3, 3))

        # q as scalar
        q = KerasTensor(())
        self.assertEqual(knp.quantile(x, q).shape, ())

        # q as 1D tensor
        q = KerasTensor((2,))
        self.assertEqual(knp.quantile(x, q).shape, (2,))
        self.assertEqual(knp.quantile(x, q, axis=1).shape, (2, 3))
        self.assertEqual(
            knp.quantile(x, q, axis=1, keepdims=True).shape,
            (2, 3, 1),
        )

    def test_take(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.take(x, 1).shape, ())
        self.assertEqual(knp.take(x, [1, 2]).shape, (2,))
        self.assertEqual(knp.take(x, [[1, 2], [1, 2]], axis=1).shape, (2, 2, 2))

        # test with multi-dimensional indices
        x = KerasTensor((2, 3, 4, 5))
        indices = KerasTensor((6, 7))
        self.assertEqual(knp.take(x, indices, axis=2).shape, (2, 3, 6, 7, 5))

    def test_take_along_axis(self):
        x = KerasTensor((2, 3))
        indices = KerasTensor((1, 3))
        self.assertEqual(knp.take_along_axis(x, indices, axis=0).shape, (1, 3))
        self.assertEqual(knp.take_along_axis(x, indices, axis=1).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            indices = KerasTensor((1, 4))
            knp.take_along_axis(x, indices, axis=0)

    def test_tensordot(self):
        x = KerasTensor((2, 3, 3))
        y = KerasTensor((3, 3, 4))
        self.assertEqual(knp.tensordot(x, y, axes=1).shape, (2, 3, 3, 4))
        self.assertEqual(knp.tensordot(x, y, axes=2).shape, (2, 4))
        self.assertEqual(
            knp.tensordot(x, y, axes=[[1, 2], [0, 1]]).shape, (2, 4)
        )

    def test_vdot(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.vdot(x, y).shape, ())

    def test_where(self):
        condition = KerasTensor((2, 3))
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.where(condition, x, y).shape, (2, 3))
        self.assertAllEqual(knp.where(condition).shape, (2, 3))

    def test_floordiv(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.floor_divide(x, y).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.floor_divide(x, y)

    def test_xor(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.logical_xor(x, y).shape, (2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3, 4))
            knp.logical_xor(x, y)

    def test_digitize(self):
        x = KerasTensor((2, 3))
        bins = KerasTensor((3,))
        self.assertEqual(knp.digitize(x, bins).shape, (2, 3))
        self.assertTrue(knp.digitize(x, bins).dtype == "int32")

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            bins = KerasTensor((2, 3, 4))
            knp.digitize(x, bins)


class NumpyOneInputOpsDynamicShapeTest(testing.TestCase):
    def test_mean(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.mean(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.mean(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.mean(x, axis=1, keepdims=True).shape, (None, 1, 3))

    def test_all(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.all(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.all(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.all(x, axis=1, keepdims=True).shape, (None, 1, 3))

    def test_any(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.any(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.any(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.any(x, axis=1, keepdims=True).shape, (None, 1, 3))

    def test_var(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.var(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.var(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.var(x, axis=1, keepdims=True).shape, (None, 1, 3))

    def test_sum(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.sum(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.sum(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.sum(x, axis=1, keepdims=True).shape, (None, 1, 3))

    def test_amax(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.amax(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.amax(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.amax(x, axis=1, keepdims=True).shape, (None, 1, 3))

    def test_amin(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.amin(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.amin(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.amin(x, axis=1, keepdims=True).shape, (None, 1, 3))

    def test_square(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.square(x).shape, (None, 3))

    def test_negative(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.negative(x).shape, (None, 3))

    def test_abs(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.abs(x).shape, (None, 3))

    def test_absolute(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.absolute(x).shape, (None, 3))

    def test_squeeze(self):
        x = KerasTensor((None, 1))
        self.assertEqual(knp.squeeze(x).shape, (None,))
        self.assertEqual(knp.squeeze(x, axis=1).shape, (None,))

        with self.assertRaises(ValueError):
            x = KerasTensor((None, 1))
            knp.squeeze(x, axis=0)

    def test_transpose(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.transpose(x).shape, (3, None))

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.transpose(x, (2, 0, 1)).shape, (3, None, 3))

    def test_arccos(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.arccos(x).shape, (None, 3))

    def test_arccosh(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.arccosh(x).shape, (None, 3))

    def test_arcsin(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.arcsin(x).shape, (None, 3))

    def test_arcsinh(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.arcsinh(x).shape, (None, 3))

    def test_arctan(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.arctan(x).shape, (None, 3))

    def test_arctanh(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.arctanh(x).shape, (None, 3))

    def test_argmax(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.argmax(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.argmax(x, axis=1).shape, (None, 3))

    def test_argmin(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.argmin(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.argmin(x, axis=1).shape, (None, 3))

    def test_argsort(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.argsort(x).shape, (None, 3))

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.argsort(x, axis=1).shape, (None, 3, 3))

    def test_array(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.array(x).shape, (None, 3))

    def test_average(self):
        x = KerasTensor((None, 3))
        weights = KerasTensor((None, 3))
        self.assertEqual(knp.average(x, weights=weights).shape, ())

        x = KerasTensor((None, 3))
        weights = KerasTensor((3,))
        self.assertEqual(knp.average(x, axis=1, weights=weights).shape, (None,))

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.average(x, axis=1).shape, (None, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((None, 3, 3))
            weights = KerasTensor((None, 4))
            knp.average(x, weights=weights)

    def test_broadcast_to(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.broadcast_to(x, (2, 3, 3)).shape, (2, 3, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((3, 3))
            knp.broadcast_to(x, (2, 2, 3))

    def test_ceil(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.ceil(x).shape, (None, 3))

    def test_clip(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.clip(x, 1, 2).shape, (None, 3))

    def test_concatenate(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((None, 3))
        self.assertEqual(
            knp.concatenate(
                [x, y],
            ).shape,
            (None, 3),
        )
        self.assertEqual(knp.concatenate([x, y], axis=1).shape, (None, 6))

        with self.assertRaises(ValueError):
            self.assertEqual(knp.concatenate([x, y], axis=None).shape, (None,))

        with self.assertRaises(ValueError):
            x = KerasTensor((None, 3, 5))
            y = KerasTensor((None, 4, 6))
            knp.concatenate([x, y], axis=1)

    def test_concatenate_sparse(self):
        x = KerasTensor((2, 3), sparse=True)
        y = KerasTensor((2, 3))
        result = knp.concatenate([x, y], axis=1)
        self.assertEqual(result.shape, (2, 6))
        self.assertFalse(result.sparse)

        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3), sparse=True)
        result = knp.concatenate([x, y], axis=1)
        self.assertEqual(result.shape, (2, 6))
        self.assertFalse(result.sparse)

        x = KerasTensor((2, 3), sparse=True)
        y = KerasTensor((2, 3), sparse=True)
        result = knp.concatenate([x, y], axis=1)
        self.assertEqual(result.shape, (2, 6))
        self.assertTrue(result.sparse)

    def test_conjugate(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.conjugate(x).shape, (None, 3))

    def test_conj(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.conj(x).shape, (None, 3))

    def test_copy(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.copy(x).shape, (None, 3))

    def test_cos(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.cos(x).shape, (None, 3))

    def test_cosh(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.cosh(x).shape, (None, 3))

    def test_count_nonzero(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.count_nonzero(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.count_nonzero(x, axis=1).shape, (None, 3))

    def test_cumprod(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.cumprod(x).shape, (None,))

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.cumprod(x, axis=1).shape, (None, 3, 3))

    def test_cumsum(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.cumsum(x).shape, (None,))

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.cumsum(x, axis=1).shape, (None, 3, 3))

    def test_diag(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.diag(x).shape, (None,))
        self.assertEqual(knp.diag(x, k=3).shape, (None,))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3, 4))
            knp.diag(x)

    def test_diagonal(self):
        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.diagonal(x).shape, (3, None))

    def test_diff(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.diff(x).shape, (None, 2))
        self.assertEqual(knp.diff(x, n=2).shape, (None, 1))
        self.assertEqual(knp.diff(x, n=3).shape, (None, 0))
        self.assertEqual(knp.diff(x, n=4).shape, (None, 0))

        self.assertEqual(knp.diff(x, axis=0).shape, (None, 3))
        self.assertEqual(knp.diff(x, n=2, axis=0).shape, (None, 3))

    def test_dot(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((3, 2))
        z = KerasTensor((None, None, 2))
        self.assertEqual(knp.dot(x, y).shape, (None, 2))
        self.assertEqual(knp.dot(x, 2).shape, (None, 3))
        self.assertEqual(knp.dot(x, z).shape, (None, None, 2))

        x = KerasTensor((None,))
        y = KerasTensor((5,))
        self.assertEqual(knp.dot(x, y).shape, ())

    def test_exp(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.exp(x).shape, (None, 3))

    def test_expand_dims(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.expand_dims(x, -1).shape, (None, 3, 1))
        self.assertEqual(knp.expand_dims(x, 0).shape, (1, None, 3))
        self.assertEqual(knp.expand_dims(x, 1).shape, (None, 1, 3))
        self.assertEqual(knp.expand_dims(x, -2).shape, (None, 1, 3))

    def test_expm1(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.expm1(x).shape, (None, 3))

    def test_flip(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.flip(x).shape, (None, 3))

    def test_floor(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.floor(x).shape, (None, 3))

    def test_get_item(self):
        x = KerasTensor((None, 5, 16))
        # Simple slice.
        sliced = knp.get_item(x, 5)
        self.assertEqual(sliced.shape, (5, 16))
        # Ellipsis slice.
        sliced = knp.get_item(x, np.s_[..., -1])
        self.assertEqual(sliced.shape, (None, 5))
        # `newaxis` slice.
        sliced = knp.get_item(x, np.s_[:, np.newaxis, ...])
        self.assertEqual(sliced.shape, (None, 1, 5, 16))
        # Strided slice.
        sliced = knp.get_item(x, np.s_[:5, 3:, 3:12:2])
        self.assertEqual(sliced.shape, (None, 2, 5))
        # Error states.
        with self.assertRaises(ValueError):
            sliced = knp.get_item(x, np.s_[:, 17, :])
        with self.assertRaises(ValueError):
            sliced = knp.get_item(x, np.s_[..., 5, ...])
        with self.assertRaises(ValueError):
            sliced = knp.get_item(x, np.s_[:, :, :, :])

    def test_hstack(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((None, 3))
        self.assertEqual(knp.hstack([x, y]).shape, (None, 6))

        x = KerasTensor((None, 3))
        y = KerasTensor((None, None))
        self.assertEqual(knp.hstack([x, y]).shape, (None, None))

    def test_imag(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.imag(x).shape, (None, 3))

    def test_isfinite(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.isfinite(x).shape, (None, 3))

    def test_isinf(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.isinf(x).shape, (None, 3))

    def test_isnan(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.isnan(x).shape, (None, 3))

    def test_log(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.log(x).shape, (None, 3))

    def test_log10(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.log10(x).shape, (None, 3))

    def test_log1p(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.log1p(x).shape, (None, 3))

    def test_log2(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.log2(x).shape, (None, 3))

    def test_logaddexp(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.logaddexp(x, x).shape, (None, 3))

    def test_logical_not(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.logical_not(x).shape, (None, 3))

    def test_max(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.max(x).shape, ())

    def test_median(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.median(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.median(x, axis=1).shape, (None, 3))
        self.assertEqual(
            knp.median(x, axis=1, keepdims=True).shape, (None, 1, 3)
        )

    def test_meshgrid(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((None, 3))
        self.assertEqual(knp.meshgrid(x, y)[0].shape, (None, None))
        self.assertEqual(knp.meshgrid(x, y)[1].shape, (None, None))

        with self.assertRaises(ValueError):
            knp.meshgrid(x, y, indexing="kk")

    def test_moveaxis(self):
        x = KerasTensor((None, 3, 4, 5))
        self.assertEqual(knp.moveaxis(x, 0, -1).shape, (3, 4, 5, None))
        self.assertEqual(knp.moveaxis(x, -1, 0).shape, (5, None, 3, 4))
        self.assertEqual(
            knp.moveaxis(x, [0, 1], [-1, -2]).shape, (4, 5, 3, None)
        )
        self.assertEqual(knp.moveaxis(x, [0, 1], [1, 0]).shape, (3, None, 4, 5))
        self.assertEqual(
            knp.moveaxis(x, [0, 1], [-2, -1]).shape, (4, 5, None, 3)
        )

    def test_ndim(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.ndim(x).shape, (2,))

    def test_ones_like(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.ones_like(x).shape, (None, 3))
        self.assertEqual(knp.ones_like(x).dtype, x.dtype)

    def test_zeros_like(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.zeros_like(x).shape, (None, 3))
        self.assertEqual(knp.zeros_like(x).dtype, x.dtype)

    def test_pad(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.pad(x, 1).shape, (None, 5))
        self.assertEqual(knp.pad(x, (1, 2)).shape, (None, 6))
        self.assertEqual(knp.pad(x, ((1, 2), (3, 4))).shape, (None, 10))

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.pad(x, 1).shape, (None, 5, 5))
        self.assertEqual(knp.pad(x, (1, 2)).shape, (None, 6, 6))
        self.assertEqual(
            knp.pad(x, ((1, 2), (3, 4), (5, 6))).shape, (None, 10, 14)
        )

    def test_prod(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.prod(x).shape, ())
        self.assertEqual(knp.prod(x, axis=0).shape, (3,))
        self.assertEqual(knp.prod(x, axis=1, keepdims=True).shape, (None, 1))

    def test_ravel(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.ravel(x).shape, (None,))

    def test_real(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.real(x).shape, (None, 3))

    def test_reciprocal(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.reciprocal(x).shape, (None, 3))

    def test_repeat(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.repeat(x, 2).shape, (None,))
        self.assertEqual(knp.repeat(x, 3, axis=1).shape, (None, 9))
        self.assertEqual(knp.repeat(x, [1, 2], axis=0).shape, (3, 3))
        self.assertEqual(knp.repeat(x, 2, axis=0).shape, (None, 3))

    def test_reshape(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.reshape(x, (3, 2)).shape, (3, 2))
        self.assertEqual(knp.reshape(x, (3, -1)).shape, (3, None))

    def test_reshape_sparse(self):
        x = KerasTensor((None, 3), sparse=True)
        self.assertTrue(knp.reshape(x, (3, 2)).sparse)
        self.assertEqual(knp.reshape(x, (3, 2)).shape, (3, 2))
        self.assertTrue(knp.reshape(x, (3, -1)).sparse)
        self.assertEqual(knp.reshape(x, (3, -1)).shape, (3, None))

    def test_roll(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.roll(x, 1).shape, (None, 3))
        self.assertEqual(knp.roll(x, 1, axis=1).shape, (None, 3))
        self.assertEqual(knp.roll(x, 1, axis=0).shape, (None, 3))

    def test_round(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.round(x).shape, (None, 3))

    def test_sign(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.sign(x).shape, (None, 3))

    def test_sin(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.sin(x).shape, (None, 3))

    def test_sinh(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.sinh(x).shape, (None, 3))

    def test_size(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.size(x).shape, ())

    def test_sort(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.sort(x).shape, (None, 3))
        self.assertEqual(knp.sort(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.sort(x, axis=0).shape, (None, 3))

    def test_split(self):
        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.split(x, 2)[0].shape, (None, 3, 3))
        self.assertEqual(knp.split(x, 3, axis=1)[0].shape, (None, 1, 3))
        self.assertEqual(len(knp.split(x, [1, 3], axis=1)), 3)
        self.assertEqual(knp.split(x, [1, 3], axis=1)[0].shape, (None, 1, 3))
        self.assertEqual(knp.split(x, [1, 3], axis=1)[1].shape, (None, 2, 3))
        self.assertEqual(knp.split(x, [1, 3], axis=1)[2].shape, (None, 0, 3))

    def test_sqrt(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.sqrt(x).shape, (None, 3))

    def test_stack(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((None, 3))
        self.assertEqual(knp.stack([x, y]).shape, (2, None, 3))
        self.assertEqual(knp.stack([x, y], axis=-1).shape, (None, 3, 2))

    def test_std(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.std(x).shape, ())

        x = KerasTensor((None, 3, 3))
        self.assertEqual(knp.std(x, axis=1).shape, (None, 3))
        self.assertEqual(knp.std(x, axis=1, keepdims=True).shape, (None, 1, 3))

    def test_swapaxes(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.swapaxes(x, 0, 1).shape, (3, None))

    def test_tan(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.tan(x).shape, (None, 3))

    def test_tanh(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.tanh(x).shape, (None, 3))

    def test_tile(self):
        x = KerasTensor((None, 3))
        self.assertEqual(knp.tile(x, [2]).shape, (None, 6))
        self.assertEqual(knp.tile(x, [1, 2]).shape, (None, 6))
        self.assertEqual(knp.tile(x, [2, 1, 2]).shape, (2, None, 6))

    def test_trace(self):
        x = KerasTensor((None, 3, None, 5))
        self.assertEqual(knp.trace(x).shape, (None, 5))
        self.assertEqual(knp.trace(x, axis1=2, axis2=3).shape, (None, 3))

    def test_tril(self):
        x = KerasTensor((None, 3, None, 5))
        self.assertEqual(knp.tril(x).shape, (None, 3, None, 5))
        self.assertEqual(knp.tril(x, k=1).shape, (None, 3, None, 5))
        self.assertEqual(knp.tril(x, k=-1).shape, (None, 3, None, 5))

    def test_triu(self):
        x = KerasTensor((None, 3, None, 5))
        self.assertEqual(knp.triu(x).shape, (None, 3, None, 5))
        self.assertEqual(knp.triu(x, k=1).shape, (None, 3, None, 5))
        self.assertEqual(knp.triu(x, k=-1).shape, (None, 3, None, 5))

    def test_vstack(self):
        x = KerasTensor((None, 3))
        y = KerasTensor((None, 3))
        self.assertEqual(knp.vstack([x, y]).shape, (None, 3))

        x = KerasTensor((None, 3))
        y = KerasTensor((None, None))
        self.assertEqual(knp.vstack([x, y]).shape, (None, 3))


class NumpyOneInputOpsStaticShapeTest(testing.TestCase):
    def test_mean(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.mean(x).shape, ())

    def test_all(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.all(x).shape, ())

    def test_any(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.any(x).shape, ())

    def test_var(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.var(x).shape, ())

    def test_sum(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.sum(x).shape, ())

    def test_amax(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.amax(x).shape, ())

    def test_amin(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.amin(x).shape, ())

    def test_square(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.square(x).shape, (2, 3))

    def test_negative(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.negative(x).shape, (2, 3))

    def test_abs(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.abs(x).shape, (2, 3))

    def test_absolute(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.absolute(x).shape, (2, 3))

    def test_squeeze(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.squeeze(x).shape, (2, 3))

        x = KerasTensor((2, 1, 3))
        self.assertEqual(knp.squeeze(x).shape, (2, 3))
        self.assertEqual(knp.squeeze(x, axis=1).shape, (2, 3))
        self.assertEqual(knp.squeeze(x, axis=-2).shape, (2, 3))

        with self.assertRaises(ValueError):
            knp.squeeze(x, axis=0)

    def test_squeeze_sparse(self):
        x = KerasTensor((2, 3), sparse=True)
        self.assertTrue(knp.squeeze(x).sparse)
        self.assertEqual(knp.squeeze(x).shape, (2, 3))

        x = KerasTensor((2, 1, 3), sparse=True)
        self.assertTrue(knp.squeeze(x).sparse)
        self.assertEqual(knp.squeeze(x).shape, (2, 3))
        self.assertTrue(knp.squeeze(x, axis=1).sparse)
        self.assertEqual(knp.squeeze(x, axis=1).shape, (2, 3))
        self.assertTrue(knp.squeeze(x, axis=-2).sparse)
        self.assertEqual(knp.squeeze(x, axis=-2).shape, (2, 3))

    def test_transpose(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.transpose(x).shape, (3, 2))

    def test_transpose_sparse(self):
        x = KerasTensor((2, 3), sparse=True)
        result = knp.transpose(x)
        self.assertEqual(result.shape, (3, 2))
        self.assertTrue(result.sparse)

    def test_arccos(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.arccos(x).shape, (2, 3))

    def test_arccosh(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.arccosh(x).shape, (2, 3))

    def test_arcsin(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.arcsin(x).shape, (2, 3))

    def test_arcsinh(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.arcsinh(x).shape, (2, 3))

    def test_arctan(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.arctan(x).shape, (2, 3))

    def test_arctanh(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.arctanh(x).shape, (2, 3))

    def test_argmax(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.argmax(x).shape, ())

    def test_argmin(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.argmin(x).shape, ())

    def test_argsort(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.argsort(x).shape, (2, 3))
        self.assertEqual(knp.argsort(x, axis=None).shape, (6,))

    def test_array(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.array(x).shape, (2, 3))

    def test_average(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.average(x).shape, ())

    def test_broadcast_to(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.broadcast_to(x, (2, 2, 3)).shape, (2, 2, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((3, 3))
            knp.broadcast_to(x, (2, 2, 3))

    def test_ceil(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.ceil(x).shape, (2, 3))

    def test_clip(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.clip(x, 1, 2).shape, (2, 3))

    def test_concatenate(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.concatenate([x, y]).shape, (4, 3))
        self.assertEqual(knp.concatenate([x, y], axis=1).shape, (2, 6))

        with self.assertRaises(ValueError):
            self.assertEqual(knp.concatenate([x, y], axis=None).shape, (None,))

    def test_conjugate(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.conjugate(x).shape, (2, 3))

    def test_conj(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.conj(x).shape, (2, 3))

    def test_copy(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.copy(x).shape, (2, 3))

    def test_cos(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.cos(x).shape, (2, 3))

    def test_cosh(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.cosh(x).shape, (2, 3))

    def test_count_nonzero(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.count_nonzero(x).shape, ())

    def test_cumprod(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.cumprod(x).shape, (6,))

    def test_cumsum(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.cumsum(x).shape, (6,))

    def test_diag(self):
        x = KerasTensor((3,))
        self.assertEqual(knp.diag(x).shape, (3, 3))
        self.assertEqual(knp.diag(x, k=3).shape, (6, 6))
        self.assertEqual(knp.diag(x, k=-2).shape, (5, 5))

        x = KerasTensor((3, 5))
        self.assertEqual(knp.diag(x).shape, (3,))
        self.assertEqual(knp.diag(x, k=3).shape, (2,))
        self.assertEqual(knp.diag(x, k=-2).shape, (1,))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3, 4))
            knp.diag(x)

    def test_diagonal(self):
        x = KerasTensor((3, 3))
        self.assertEqual(knp.diagonal(x).shape, (3,))
        self.assertEqual(knp.diagonal(x, offset=1).shape, (2,))

        x = KerasTensor((3, 5, 5))
        self.assertEqual(knp.diagonal(x).shape, (5, 3))

        with self.assertRaises(ValueError):
            x = KerasTensor((3,))
            knp.diagonal(x)

    def test_diff(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.diff(x).shape, (2, 2))
        self.assertEqual(knp.diff(x, n=2).shape, (2, 1))
        self.assertEqual(knp.diff(x, n=3).shape, (2, 0))
        self.assertEqual(knp.diff(x, n=4).shape, (2, 0))

        self.assertEqual(knp.diff(x, axis=0).shape, (1, 3))
        self.assertEqual(knp.diff(x, n=2, axis=0).shape, (0, 3))
        self.assertEqual(knp.diff(x, n=3, axis=0).shape, (0, 3))

    def test_dot(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((3, 2))
        z = KerasTensor((4, 3, 2))
        self.assertEqual(knp.dot(x, y).shape, (2, 2))
        self.assertEqual(knp.dot(x, 2).shape, (2, 3))
        self.assertEqual(knp.dot(x, z).shape, (2, 4, 2))

        x = KerasTensor((5,))
        y = KerasTensor((5,))
        self.assertEqual(knp.dot(x, y).shape, ())

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((2, 3))
            knp.dot(x, y)

    def test_exp(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.exp(x).shape, (2, 3))

    def test_expand_dims(self):
        x = KerasTensor((2, 3, 4))
        self.assertEqual(knp.expand_dims(x, 0).shape, (1, 2, 3, 4))
        self.assertEqual(knp.expand_dims(x, 1).shape, (2, 1, 3, 4))
        self.assertEqual(knp.expand_dims(x, -2).shape, (2, 3, 1, 4))

    def test_expand_dims_sparse(self):
        x = KerasTensor((2, 3, 4), sparse=True)
        self.assertTrue(knp.expand_dims(x, 0).sparse)
        self.assertEqual(knp.expand_dims(x, 0).shape, (1, 2, 3, 4))
        self.assertTrue(knp.expand_dims(x, 1).sparse)
        self.assertEqual(knp.expand_dims(x, 1).shape, (2, 1, 3, 4))
        self.assertTrue(knp.expand_dims(x, -2).sparse)
        self.assertEqual(knp.expand_dims(x, -2).shape, (2, 3, 1, 4))

    def test_expm1(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.expm1(x).shape, (2, 3))

    def test_flip(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.flip(x).shape, (2, 3))

    def test_floor(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.floor(x).shape, (2, 3))

    def test_get_item(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.get_item(x, 1).shape, (3,))

        x = KerasTensor((5, 3, 2))
        self.assertEqual(knp.get_item(x, 3).shape, (3, 2))

        x = KerasTensor(
            [
                2,
            ]
        )
        self.assertEqual(knp.get_item(x, 0).shape, ())

    def test_hstack(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.hstack([x, y]).shape, (2, 6))

    def test_imag(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.imag(x).shape, (2, 3))

    def test_isfinite(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.isfinite(x).shape, (2, 3))

    def test_isinf(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.isinf(x).shape, (2, 3))

    def test_isnan(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.isnan(x).shape, (2, 3))

    def test_log(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.log(x).shape, (2, 3))

    def test_log10(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.log10(x).shape, (2, 3))

    def test_log1p(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.log1p(x).shape, (2, 3))

    def test_log2(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.log2(x).shape, (2, 3))

    def test_logaddexp(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.logaddexp(x, x).shape, (2, 3))

    def test_logical_not(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.logical_not(x).shape, (2, 3))

    def test_max(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.max(x).shape, ())

    def test_median(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.median(x).shape, ())

        x = KerasTensor((2, 3, 3))
        self.assertEqual(knp.median(x, axis=1).shape, (2, 3))
        self.assertEqual(knp.median(x, axis=1, keepdims=True).shape, (2, 1, 3))

    def test_meshgrid(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3, 4))
        z = KerasTensor((2, 3, 4, 5))
        self.assertEqual(knp.meshgrid(x, y)[0].shape, (24, 6))
        self.assertEqual(knp.meshgrid(x, y)[1].shape, (24, 6))
        self.assertEqual(knp.meshgrid(x, y, indexing="ij")[0].shape, (6, 24))
        self.assertEqual(
            knp.meshgrid(x, y, z, indexing="ij")[0].shape, (6, 24, 120)
        )
        with self.assertRaises(ValueError):
            knp.meshgrid(x, y, indexing="kk")

    def test_moveaxis(self):
        x = KerasTensor((2, 3, 4, 5))
        self.assertEqual(knp.moveaxis(x, 0, -1).shape, (3, 4, 5, 2))
        self.assertEqual(knp.moveaxis(x, -1, 0).shape, (5, 2, 3, 4))
        self.assertEqual(knp.moveaxis(x, [0, 1], [-1, -2]).shape, (4, 5, 3, 2))
        self.assertEqual(knp.moveaxis(x, [0, 1], [1, 0]).shape, (3, 2, 4, 5))
        self.assertEqual(knp.moveaxis(x, [0, 1], [-2, -1]).shape, (4, 5, 2, 3))

    def test_ndim(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.ndim(x).shape, (2,))

    def test_ones_like(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.ones_like(x).shape, (2, 3))
        self.assertEqual(knp.ones_like(x).dtype, x.dtype)

    def test_zeros_like(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.zeros_like(x).shape, (2, 3))
        self.assertEqual(knp.zeros_like(x).dtype, x.dtype)

    def test_pad(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.pad(x, 1).shape, (4, 5))
        self.assertEqual(knp.pad(x, (1, 2)).shape, (5, 6))
        self.assertEqual(knp.pad(x, ((1, 2), (3, 4))).shape, (5, 10))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            knp.pad(x, ((1, 2), (3, 4), (5, 6)))

    def test_prod(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.prod(x).shape, ())
        self.assertEqual(knp.prod(x, axis=0).shape, (3,))
        self.assertEqual(knp.prod(x, axis=1).shape, (2,))

    def test_ravel(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.ravel(x).shape, (6,))

    def test_real(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.real(x).shape, (2, 3))

    def test_reciprocal(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.reciprocal(x).shape, (2, 3))

    def test_repeat(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.repeat(x, 2).shape, (12,))
        self.assertEqual(knp.repeat(x, 3, axis=1).shape, (2, 9))
        self.assertEqual(knp.repeat(x, [1, 2], axis=0).shape, (3, 3))

    def test_reshape(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.reshape(x, (3, 2)).shape, (3, 2))
        self.assertEqual(knp.reshape(x, (3, -1)).shape, (3, 2))
        self.assertEqual(knp.reshape(x, (6,)).shape, (6,))
        self.assertEqual(knp.reshape(x, (-1,)).shape, (6,))

    def test_reshape_sparse(self):
        x = KerasTensor((2, 3), sparse=True)

        result = knp.reshape(x, (3, 2))
        self.assertEqual(result.shape, (3, 2))
        self.assertTrue(result.sparse)

        result = knp.reshape(x, (3, -1))
        self.assertEqual(result.shape, (3, 2))
        self.assertTrue(result.sparse)

        result = knp.reshape(x, (6,))
        self.assertEqual(result.shape, (6,))
        self.assertTrue(result.sparse)

        result = knp.reshape(x, (-1,))
        self.assertEqual(result.shape, (6,))
        self.assertTrue(result.sparse)

    def test_roll(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.roll(x, 1).shape, (2, 3))
        self.assertEqual(knp.roll(x, 1, axis=1).shape, (2, 3))
        self.assertEqual(knp.roll(x, 1, axis=0).shape, (2, 3))

    def test_round(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.round(x).shape, (2, 3))

    def test_sign(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.sign(x).shape, (2, 3))

    def test_sin(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.sin(x).shape, (2, 3))

    def test_sinh(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.sinh(x).shape, (2, 3))

    def test_size(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.size(x).shape, ())

    def test_sort(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.sort(x).shape, (2, 3))
        self.assertEqual(knp.sort(x, axis=1).shape, (2, 3))
        self.assertEqual(knp.sort(x, axis=0).shape, (2, 3))

    def test_split(self):
        x = KerasTensor((2, 3))
        self.assertEqual(len(knp.split(x, 2)), 2)
        self.assertEqual(knp.split(x, 2)[0].shape, (1, 3))
        self.assertEqual(knp.split(x, 3, axis=1)[0].shape, (2, 1))
        self.assertEqual(len(knp.split(x, [1, 3], axis=1)), 3)
        self.assertEqual(knp.split(x, [1, 3], axis=1)[0].shape, (2, 1))
        self.assertEqual(knp.split(x, [1, 3], axis=1)[1].shape, (2, 2))
        self.assertEqual(knp.split(x, [1, 3], axis=1)[2].shape, (2, 0))

        with self.assertRaises(ValueError):
            knp.split(x, 2, axis=1)

    def test_sqrt(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.sqrt(x).shape, (2, 3))

    def test_stack(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.stack([x, y]).shape, (2, 2, 3))
        self.assertEqual(knp.stack([x, y], axis=-1).shape, (2, 3, 2))

        with self.assertRaises(ValueError):
            x = KerasTensor((2, 3))
            y = KerasTensor((3, 3))
            knp.stack([x, y])

    def test_std(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.std(x).shape, ())

    def test_swapaxes(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.swapaxes(x, 0, 1).shape, (3, 2))

    def test_tan(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.tan(x).shape, (2, 3))

    def test_tanh(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.tanh(x).shape, (2, 3))

    def test_tile(self):
        x = KerasTensor((2, 3))
        self.assertEqual(knp.tile(x, [2]).shape, (2, 6))
        self.assertEqual(knp.tile(x, [1, 2]).shape, (2, 6))
        self.assertEqual(knp.tile(x, [2, 1, 2]).shape, (2, 2, 6))

    def test_trace(self):
        x = KerasTensor((2, 3, 4, 5))
        self.assertEqual(knp.trace(x).shape, (4, 5))
        self.assertEqual(knp.trace(x, axis1=2, axis2=3).shape, (2, 3))

    def test_tril(self):
        x = KerasTensor((2, 3, 4, 5))
        self.assertEqual(knp.tril(x).shape, (2, 3, 4, 5))
        self.assertEqual(knp.tril(x, k=1).shape, (2, 3, 4, 5))
        self.assertEqual(knp.tril(x, k=-1).shape, (2, 3, 4, 5))

    def test_triu(self):
        x = KerasTensor((2, 3, 4, 5))
        self.assertEqual(knp.triu(x).shape, (2, 3, 4, 5))
        self.assertEqual(knp.triu(x, k=1).shape, (2, 3, 4, 5))
        self.assertEqual(knp.triu(x, k=-1).shape, (2, 3, 4, 5))

    def test_vstack(self):
        x = KerasTensor((2, 3))
        y = KerasTensor((2, 3))
        self.assertEqual(knp.vstack([x, y]).shape, (4, 3))


class NumpyTwoInputOpsCorretnessTest(testing.TestCase, parameterized.TestCase):
    def test_add(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        z = np.array([[[1, 2, 3], [3, 2, 1]]])
        self.assertAllClose(knp.add(x, y), np.add(x, y))
        self.assertAllClose(knp.add(x, z), np.add(x, z))

        self.assertAllClose(knp.Add()(x, y), np.add(x, y))
        self.assertAllClose(knp.Add()(x, z), np.add(x, z))

    def test_subtract(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        z = np.array([[[1, 2, 3], [3, 2, 1]]])
        self.assertAllClose(knp.subtract(x, y), np.subtract(x, y))
        self.assertAllClose(knp.subtract(x, z), np.subtract(x, z))

        self.assertAllClose(knp.Subtract()(x, y), np.subtract(x, y))
        self.assertAllClose(knp.Subtract()(x, z), np.subtract(x, z))

    def test_multiply(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        z = np.array([[[1, 2, 3], [3, 2, 1]]])
        self.assertAllClose(knp.multiply(x, y), np.multiply(x, y))
        self.assertAllClose(knp.multiply(x, z), np.multiply(x, z))

        self.assertAllClose(knp.Multiply()(x, y), np.multiply(x, y))
        self.assertAllClose(knp.Multiply()(x, z), np.multiply(x, z))

    def test_matmul(self):
        x = np.ones([2, 3, 4, 5])
        y = np.ones([2, 3, 5, 6])
        z = np.ones([5, 6])
        self.assertAllClose(knp.matmul(x, y), np.matmul(x, y))
        self.assertAllClose(knp.matmul(x, z), np.matmul(x, z))

        self.assertAllClose(knp.Matmul()(x, y), np.matmul(x, y))
        self.assertAllClose(knp.Matmul()(x, z), np.matmul(x, z))

    @parameterized.named_parameters(
        named_product(
            (
                {
                    "testcase_name": "rank2",
                    "x_shape": (5, 3),
                    "y_shape": (3, 4),
                },
                {
                    "testcase_name": "rank3",
                    "x_shape": (2, 5, 3),
                    "y_shape": (2, 3, 4),
                },
                {
                    "testcase_name": "rank4",
                    "x_shape": (2, 2, 5, 3),
                    "y_shape": (2, 2, 3, 4),
                },
            ),
            dtype=["float16", "float32", "float64", "int32"],
            x_sparse=[False, True],
            y_sparse=[False, True],
        )
    )
    @pytest.mark.skipif(
        not backend.SUPPORTS_SPARSE_TENSORS,
        reason="Backend does not support sparse tensors.",
    )
    def test_matmul_sparse(self, dtype, x_shape, y_shape, x_sparse, y_sparse):
        import tensorflow as tf

        if x_sparse and y_sparse and dtype in ("float16", "int32"):
            pytest.skip(f"Sparse sparse matmul unsupported for {dtype}")

        rng = np.random.default_rng(0)
        if x_sparse:
            x_np = (4 * rng.standard_normal(x_shape)).astype(dtype)
            x_np = np.multiply(x_np, rng.random(x_shape) < 0.7)
            x = tf.sparse.from_dense(x_np)
        else:
            x = x_np = (4 * rng.standard_normal(x_shape)).astype(dtype)
        y = y_np = (4 * rng.standard_normal(y_shape)).astype(dtype)
        if y_sparse:
            y_np = (4 * rng.standard_normal(y_shape)).astype(dtype)
            y_np = np.multiply(y_np, rng.random(y_shape) < 0.7)
            y = tf.sparse.from_dense(y_np)
        else:
            y = y_np = (4 * rng.standard_normal(y_shape)).astype(dtype)

        atol = 0.1 if dtype == "float16" else 1e-4
        self.assertAllClose(knp.matmul(x, y), np.matmul(x_np, y_np), atol=atol)
        if x_sparse and y_sparse:
            self.assertIsInstance(knp.matmul(x, y), tf.SparseTensor)

    def test_power(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        z = np.array([[[1, 2, 3], [3, 2, 1]]])
        self.assertAllClose(knp.power(x, y), np.power(x, y))
        self.assertAllClose(knp.power(x, z), np.power(x, z))

        self.assertAllClose(knp.Power()(x, y), np.power(x, y))
        self.assertAllClose(knp.Power()(x, z), np.power(x, z))

    def test_divide(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        z = np.array([[[1, 2, 3], [3, 2, 1]]])
        self.assertAllClose(knp.divide(x, y), np.divide(x, y))
        self.assertAllClose(knp.divide(x, z), np.divide(x, z))

        self.assertAllClose(knp.Divide()(x, y), np.divide(x, y))
        self.assertAllClose(knp.Divide()(x, z), np.divide(x, z))

    def test_true_divide(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        z = np.array([[[1, 2, 3], [3, 2, 1]]])
        self.assertAllClose(knp.true_divide(x, y), np.true_divide(x, y))
        self.assertAllClose(knp.true_divide(x, z), np.true_divide(x, z))

        self.assertAllClose(knp.TrueDivide()(x, y), np.true_divide(x, y))
        self.assertAllClose(knp.TrueDivide()(x, z), np.true_divide(x, z))

    def test_append(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        z = np.array([[[1, 2, 3], [3, 2, 1]], [[4, 5, 6], [3, 2, 1]]])
        self.assertAllClose(knp.append(x, y), np.append(x, y))
        self.assertAllClose(knp.append(x, y, axis=1), np.append(x, y, axis=1))
        self.assertAllClose(knp.append(x, z), np.append(x, z))

        self.assertAllClose(knp.Append()(x, y), np.append(x, y))
        self.assertAllClose(knp.Append(axis=1)(x, y), np.append(x, y, axis=1))
        self.assertAllClose(knp.Append()(x, z), np.append(x, z))

    def test_arctan2(self):
        x = np.array([[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]])
        y = np.array([[4.0, 5.0, 6.0], [3.0, 2.0, 1.0]])
        self.assertAllClose(knp.arctan2(x, y), np.arctan2(x, y))

        self.assertAllClose(knp.Arctan2()(x, y), np.arctan2(x, y))

    def test_cross(self):
        x1 = np.ones([2, 1, 4, 3])
        x2 = np.ones([2, 1, 4, 2])
        y1 = np.ones([2, 1, 4, 3])
        y2 = np.ones([1, 5, 4, 3])
        y3 = np.ones([1, 5, 4, 2])
        self.assertAllClose(knp.cross(x1, y1), np.cross(x1, y1))
        self.assertAllClose(knp.cross(x1, y2), np.cross(x1, y2))
        if backend.backend() != "torch":
            # API divergence between `torch.cross` and `np.cross`
            # `torch.cross` only allows dim 3, `np.cross` allows dim 2 or 3
            self.assertAllClose(knp.cross(x1, y3), np.cross(x1, y3))
            self.assertAllClose(knp.cross(x2, y3), np.cross(x2, y3))

        self.assertAllClose(knp.Cross()(x1, y1), np.cross(x1, y1))
        self.assertAllClose(knp.Cross()(x1, y2), np.cross(x1, y2))
        if backend.backend() != "torch":
            # API divergence between `torch.cross` and `np.cross`
            # `torch.cross` only allows dim 3, `np.cross` allows dim 2 or 3
            self.assertAllClose(knp.Cross()(x1, y3), np.cross(x1, y3))
            self.assertAllClose(knp.Cross()(x2, y3), np.cross(x2, y3))

    def test_einsum(self):
        x = np.arange(24).reshape([2, 3, 4]).astype("float32")
        y = np.arange(24).reshape([2, 4, 3]).astype("float32")
        self.assertAllClose(
            knp.einsum("ijk,lkj->il", x, y),
            np.einsum("ijk,lkj->il", x, y),
        )
        self.assertAllClose(
            knp.einsum("ijk,ikj->i", x, y),
            np.einsum("ijk,ikj->i", x, y),
        )
        self.assertAllClose(
            knp.einsum("i...,j...k->...ijk", x, y),
            np.einsum("i..., j...k->...ijk", x, y),
        )
        self.assertAllClose(knp.einsum(",ijk", 5, y), np.einsum(",ijk", 5, y))

        self.assertAllClose(
            knp.Einsum("ijk,lkj->il")(x, y),
            np.einsum("ijk,lkj->il", x, y),
        )
        self.assertAllClose(
            knp.Einsum("ijk,ikj->i")(x, y),
            np.einsum("ijk,ikj->i", x, y),
        )
        self.assertAllClose(
            knp.Einsum("i...,j...k->...ijk")(x, y),
            np.einsum("i...,j...k->...ijk", x, y),
        )
        self.assertAllClose(knp.Einsum(",ijk")(5, y), np.einsum(",ijk", 5, y))

    def test_full_like(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.full_like(x, 2), np.full_like(x, 2))
        self.assertAllClose(
            knp.full_like(x, 2, dtype="float32"),
            np.full_like(x, 2, dtype="float32"),
        )
        self.assertAllClose(
            knp.full_like(x, np.ones([2, 3])),
            np.full_like(x, np.ones([2, 3])),
        )

        self.assertAllClose(knp.FullLike()(x, 2), np.full_like(x, 2))
        self.assertAllClose(
            knp.FullLike()(x, 2, dtype="float32"),
            np.full_like(x, 2, dtype="float32"),
        )
        self.assertAllClose(
            knp.FullLike()(x, np.ones([2, 3])),
            np.full_like(x, np.ones([2, 3])),
        )

    def test_greater(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        self.assertAllClose(knp.greater(x, y), np.greater(x, y))
        self.assertAllClose(knp.greater(x, 2), np.greater(x, 2))
        self.assertAllClose(knp.greater(2, x), np.greater(2, x))

        self.assertAllClose(knp.Greater()(x, y), np.greater(x, y))
        self.assertAllClose(knp.Greater()(x, 2), np.greater(x, 2))
        self.assertAllClose(knp.Greater()(2, x), np.greater(2, x))

    def test_greater_equal(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        self.assertAllClose(
            knp.greater_equal(x, y),
            np.greater_equal(x, y),
        )
        self.assertAllClose(
            knp.greater_equal(x, 2),
            np.greater_equal(x, 2),
        )
        self.assertAllClose(
            knp.greater_equal(2, x),
            np.greater_equal(2, x),
        )

        self.assertAllClose(
            knp.GreaterEqual()(x, y),
            np.greater_equal(x, y),
        )
        self.assertAllClose(
            knp.GreaterEqual()(x, 2),
            np.greater_equal(x, 2),
        )
        self.assertAllClose(
            knp.GreaterEqual()(2, x),
            np.greater_equal(2, x),
        )

    def test_isclose(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        self.assertAllClose(knp.isclose(x, y), np.isclose(x, y))
        self.assertAllClose(knp.isclose(x, 2), np.isclose(x, 2))
        self.assertAllClose(knp.isclose(2, x), np.isclose(2, x))

        self.assertAllClose(knp.Isclose()(x, y), np.isclose(x, y))
        self.assertAllClose(knp.Isclose()(x, 2), np.isclose(x, 2))
        self.assertAllClose(knp.Isclose()(2, x), np.isclose(2, x))

    def test_less(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        self.assertAllClose(knp.less(x, y), np.less(x, y))
        self.assertAllClose(knp.less(x, 2), np.less(x, 2))
        self.assertAllClose(knp.less(2, x), np.less(2, x))

        self.assertAllClose(knp.Less()(x, y), np.less(x, y))
        self.assertAllClose(knp.Less()(x, 2), np.less(x, 2))
        self.assertAllClose(knp.Less()(2, x), np.less(2, x))

    def test_less_equal(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        self.assertAllClose(knp.less_equal(x, y), np.less_equal(x, y))
        self.assertAllClose(knp.less_equal(x, 2), np.less_equal(x, 2))
        self.assertAllClose(knp.less_equal(2, x), np.less_equal(2, x))

        self.assertAllClose(knp.LessEqual()(x, y), np.less_equal(x, y))
        self.assertAllClose(knp.LessEqual()(x, 2), np.less_equal(x, 2))
        self.assertAllClose(knp.LessEqual()(2, x), np.less_equal(2, x))

    def test_linspace(self):
        self.assertAllClose(knp.linspace(0, 10, 5), np.linspace(0, 10, 5))
        self.assertAllClose(
            knp.linspace(0, 10, 5, endpoint=False),
            np.linspace(0, 10, 5, endpoint=False),
        )
        self.assertAllClose(knp.Linspace(num=5)(0, 10), np.linspace(0, 10, 5))
        self.assertAllClose(
            knp.Linspace(num=5, endpoint=False)(0, 10),
            np.linspace(0, 10, 5, endpoint=False),
        )

        start = np.zeros([2, 3, 4])
        stop = np.ones([2, 3, 4])
        self.assertAllClose(
            knp.linspace(start, stop, 5, retstep=True)[0],
            np.linspace(start, stop, 5, retstep=True)[0],
        )
        self.assertAllClose(
            backend.convert_to_numpy(
                knp.linspace(start, stop, 5, endpoint=False, retstep=True)[0]
            ),
            np.linspace(start, stop, 5, endpoint=False, retstep=True)[0],
        )
        self.assertAllClose(
            backend.convert_to_numpy(
                knp.linspace(
                    start, stop, 5, endpoint=False, retstep=True, dtype="int32"
                )[0]
            ),
            np.linspace(
                start, stop, 5, endpoint=False, retstep=True, dtype="int32"
            )[0],
        )

        self.assertAllClose(
            knp.Linspace(5, retstep=True)(start, stop)[0],
            np.linspace(start, stop, 5, retstep=True)[0],
        )
        self.assertAllClose(
            backend.convert_to_numpy(
                knp.Linspace(5, endpoint=False, retstep=True)(start, stop)[0]
            ),
            np.linspace(start, stop, 5, endpoint=False, retstep=True)[0],
        )
        self.assertAllClose(
            backend.convert_to_numpy(
                knp.Linspace(5, endpoint=False, retstep=True, dtype="int32")(
                    start, stop
                )[0]
            ),
            np.linspace(
                start, stop, 5, endpoint=False, retstep=True, dtype="int32"
            )[0],
        )

    def test_logical_and(self):
        x = np.array([[True, False], [True, True]])
        y = np.array([[False, False], [True, False]])
        self.assertAllClose(knp.logical_and(x, y), np.logical_and(x, y))
        self.assertAllClose(knp.logical_and(x, True), np.logical_and(x, True))
        self.assertAllClose(knp.logical_and(True, x), np.logical_and(True, x))

        self.assertAllClose(knp.LogicalAnd()(x, y), np.logical_and(x, y))
        self.assertAllClose(knp.LogicalAnd()(x, True), np.logical_and(x, True))
        self.assertAllClose(knp.LogicalAnd()(True, x), np.logical_and(True, x))

    def test_logical_or(self):
        x = np.array([[True, False], [True, True]])
        y = np.array([[False, False], [True, False]])
        self.assertAllClose(knp.logical_or(x, y), np.logical_or(x, y))
        self.assertAllClose(knp.logical_or(x, True), np.logical_or(x, True))
        self.assertAllClose(knp.logical_or(True, x), np.logical_or(True, x))

        self.assertAllClose(knp.LogicalOr()(x, y), np.logical_or(x, y))
        self.assertAllClose(knp.LogicalOr()(x, True), np.logical_or(x, True))
        self.assertAllClose(knp.LogicalOr()(True, x), np.logical_or(True, x))

    def test_logspace(self):
        self.assertAllClose(knp.logspace(0, 10, 5), np.logspace(0, 10, 5))
        self.assertAllClose(
            knp.logspace(0, 10, 5, endpoint=False),
            np.logspace(0, 10, 5, endpoint=False),
        )
        self.assertAllClose(knp.Logspace(num=5)(0, 10), np.logspace(0, 10, 5))
        self.assertAllClose(
            knp.Logspace(num=5, endpoint=False)(0, 10),
            np.logspace(0, 10, 5, endpoint=False),
        )

        start = np.zeros([2, 3, 4])
        stop = np.ones([2, 3, 4])

        self.assertAllClose(
            knp.logspace(start, stop, 5, base=10),
            np.logspace(start, stop, 5, base=10),
        )
        self.assertAllClose(
            knp.logspace(start, stop, 5, endpoint=False, base=10),
            np.logspace(start, stop, 5, endpoint=False, base=10),
        )

        self.assertAllClose(
            knp.Logspace(5, base=10)(start, stop),
            np.logspace(start, stop, 5, base=10),
        )
        self.assertAllClose(
            knp.Logspace(5, endpoint=False, base=10)(start, stop),
            np.logspace(start, stop, 5, endpoint=False, base=10),
        )

    def test_maximum(self):
        x = np.array([[1, 2], [3, 4]])
        y = np.array([[5, 6], [7, 8]])
        self.assertAllClose(knp.maximum(x, y), np.maximum(x, y))
        self.assertAllClose(knp.maximum(x, 1), np.maximum(x, 1))
        self.assertAllClose(knp.maximum(1, x), np.maximum(1, x))

        self.assertAllClose(knp.Maximum()(x, y), np.maximum(x, y))
        self.assertAllClose(knp.Maximum()(x, 1), np.maximum(x, 1))
        self.assertAllClose(knp.Maximum()(1, x), np.maximum(1, x))

    def test_minimum(self):
        x = np.array([[1, 2], [3, 4]])
        y = np.array([[5, 6], [7, 8]])
        self.assertAllClose(knp.minimum(x, y), np.minimum(x, y))
        self.assertAllClose(knp.minimum(x, 1), np.minimum(x, 1))
        self.assertAllClose(knp.minimum(1, x), np.minimum(1, x))

        self.assertAllClose(knp.Minimum()(x, y), np.minimum(x, y))
        self.assertAllClose(knp.Minimum()(x, 1), np.minimum(x, 1))
        self.assertAllClose(knp.Minimum()(1, x), np.minimum(1, x))

    def test_mod(self):
        x = np.array([[1, 2], [3, 4]])
        y = np.array([[5, 6], [7, 8]])
        self.assertAllClose(knp.mod(x, y), np.mod(x, y))
        self.assertAllClose(knp.mod(x, 1), np.mod(x, 1))
        self.assertAllClose(knp.mod(1, x), np.mod(1, x))

        self.assertAllClose(knp.Mod()(x, y), np.mod(x, y))
        self.assertAllClose(knp.Mod()(x, 1), np.mod(x, 1))
        self.assertAllClose(knp.Mod()(1, x), np.mod(1, x))

    def test_not_equal(self):
        x = np.array([[1, 2], [3, 4]])
        y = np.array([[5, 6], [7, 8]])
        self.assertAllClose(knp.not_equal(x, y), np.not_equal(x, y))
        self.assertAllClose(knp.not_equal(x, 1), np.not_equal(x, 1))
        self.assertAllClose(knp.not_equal(1, x), np.not_equal(1, x))

        self.assertAllClose(knp.NotEqual()(x, y), np.not_equal(x, y))
        self.assertAllClose(knp.NotEqual()(x, 1), np.not_equal(x, 1))
        self.assertAllClose(knp.NotEqual()(1, x), np.not_equal(1, x))

    def test_outer(self):
        x = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        self.assertAllClose(knp.outer(x, y), np.outer(x, y))
        self.assertAllClose(knp.Outer()(x, y), np.outer(x, y))

        x = np.ones([2, 3, 4])
        y = np.ones([2, 3, 4, 5, 6])
        self.assertAllClose(knp.outer(x, y), np.outer(x, y))
        self.assertAllClose(knp.Outer()(x, y), np.outer(x, y))

    def test_quantile(self):
        x = np.arange(24).reshape([2, 3, 4]).astype("float32")

        # q as scalar
        q = np.array(0.5, dtype="float32")
        self.assertAllClose(knp.quantile(x, q), np.quantile(x, q))
        self.assertAllClose(
            knp.quantile(x, q, keepdims=True), np.quantile(x, q, keepdims=True)
        )

        # q as 1D tensor
        q = np.array([0.5, 1.0], dtype="float32")
        self.assertAllClose(knp.quantile(x, q), np.quantile(x, q))
        self.assertAllClose(
            knp.quantile(x, q, keepdims=True), np.quantile(x, q, keepdims=True)
        )
        self.assertAllClose(
            knp.quantile(x, q, axis=1), np.quantile(x, q, axis=1)
        )
        self.assertAllClose(
            knp.quantile(x, q, axis=1, keepdims=True),
            np.quantile(x, q, axis=1, keepdims=True),
        )

        # multiple axes
        self.assertAllClose(
            knp.quantile(x, q, axis=(1, 2)), np.quantile(x, q, axis=(1, 2))
        )

        # test all supported methods
        q = np.array([0.501, 1.0], dtype="float32")
        for method in ["linear", "lower", "higher", "midpoint", "nearest"]:
            self.assertAllClose(
                knp.quantile(x, q, method=method),
                np.quantile(x, q, method=method),
            )
            self.assertAllClose(
                knp.quantile(x, q, axis=1, method=method),
                np.quantile(x, q, axis=1, method=method),
            )

    def test_take(self):
        x = np.arange(24).reshape([1, 2, 3, 4])
        indices = np.array([0, 1])
        self.assertAllClose(knp.take(x, indices), np.take(x, indices))
        self.assertAllClose(knp.take(x, 0), np.take(x, 0))
        self.assertAllClose(knp.take(x, 0, axis=1), np.take(x, 0, axis=1))

        self.assertAllClose(knp.Take()(x, indices), np.take(x, indices))
        self.assertAllClose(knp.Take()(x, 0), np.take(x, 0))
        self.assertAllClose(knp.Take(axis=1)(x, 0), np.take(x, 0, axis=1))

        # test with multi-dimensional indices
        rng = np.random.default_rng(0)
        x = rng.standard_normal((2, 3, 4, 5))
        indices = rng.integers(0, 4, (6, 7))
        self.assertAllClose(
            knp.take(x, indices, axis=2),
            np.take(x, indices, axis=2),
        )

        # test with negative axis
        self.assertAllClose(
            knp.take(x, indices, axis=-2),
            np.take(x, indices, axis=-2),
        )

    @parameterized.named_parameters(
        named_product(
            [
                {"testcase_name": "axis_none", "axis": None},
                {"testcase_name": "axis_0", "axis": 0},
                {"testcase_name": "axis_1", "axis": 1},
                {"testcase_name": "axis_minus1", "axis": -1},
            ],
            dtype=[
                "float16",
                "float32",
                "float64",
                "uint8",
                "int8",
                "int16",
                "int32",
            ],
        )
    )
    @pytest.mark.skipif(
        not backend.SUPPORTS_SPARSE_TENSORS,
        reason="Backend does not support sparse tensors.",
    )
    def test_take_sparse(self, dtype, axis):
        import tensorflow as tf

        rng = np.random.default_rng(0)
        x = (4 * rng.standard_normal((3, 4, 5))).astype(dtype)
        indices = tf.SparseTensor(
            indices=[[0, 0], [1, 2]], values=[1, 2], dense_shape=(2, 3)
        )
        self.assertAllClose(
            knp.take(x, indices, axis=axis),
            np.take(x, tf.sparse.to_dense(indices).numpy(), axis=axis),
        )

    def test_take_along_axis(self):
        x = np.arange(24).reshape([1, 2, 3, 4])
        indices = np.ones([1, 4, 1, 1], dtype=np.int32)
        self.assertAllClose(
            knp.take_along_axis(x, indices, axis=1),
            np.take_along_axis(x, indices, axis=1),
        )
        self.assertAllClose(
            knp.TakeAlongAxis(axis=1)(x, indices),
            np.take_along_axis(x, indices, axis=1),
        )

        x = np.arange(12).reshape([1, 1, 3, 4])
        indices = np.ones([1, 4, 1, 1], dtype=np.int32)
        self.assertAllClose(
            knp.take_along_axis(x, indices, axis=2),
            np.take_along_axis(x, indices, axis=2),
        )
        self.assertAllClose(
            knp.TakeAlongAxis(axis=2)(x, indices),
            np.take_along_axis(x, indices, axis=2),
        )

    def test_tensordot(self):
        x = np.arange(24).reshape([1, 2, 3, 4]).astype("float32")
        y = np.arange(24).reshape([3, 4, 1, 2]).astype("float32")
        self.assertAllClose(
            knp.tensordot(x, y, axes=2), np.tensordot(x, y, axes=2)
        )
        self.assertAllClose(
            knp.tensordot(x, y, axes=([0, 1], [2, 3])),
            np.tensordot(x, y, axes=([0, 1], [2, 3])),
        )
        self.assertAllClose(
            knp.Tensordot(axes=2)(x, y),
            np.tensordot(x, y, axes=2),
        )
        self.assertAllClose(
            knp.Tensordot(axes=([0, 1], [2, 3]))(x, y),
            np.tensordot(x, y, axes=([0, 1], [2, 3])),
        )
        self.assertAllClose(
            knp.Tensordot(axes=[0, 2])(x, y),
            np.tensordot(x, y, axes=[0, 2]),
        )

    def test_vdot(self):
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([4.0, 5.0, 6.0])
        self.assertAllClose(knp.vdot(x, y), np.vdot(x, y))
        self.assertAllClose(knp.Vdot()(x, y), np.vdot(x, y))

    def test_where(self):
        x = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        self.assertAllClose(knp.where(x > 1, x, y), np.where(x > 1, x, y))
        self.assertAllClose(knp.Where()(x > 1, x, y), np.where(x > 1, x, y))
        self.assertAllClose(knp.where(x > 1), np.where(x > 1))
        self.assertAllClose(knp.Where()(x > 1), np.where(x > 1))

    def test_digitize(self):
        x = np.array([0.0, 1.0, 3.0, 1.6])
        bins = np.array([0.0, 3.0, 4.5, 7.0])
        self.assertAllClose(knp.digitize(x, bins), np.digitize(x, bins))
        self.assertAllClose(knp.Digitize()(x, bins), np.digitize(x, bins))
        self.assertTrue(
            standardize_dtype(knp.digitize(x, bins).dtype) == "int32"
        )
        self.assertTrue(
            standardize_dtype(knp.Digitize()(x, bins).dtype) == "int32"
        )

        x = np.array([0.2, 6.4, 3.0, 1.6])
        bins = np.array([0.0, 1.0, 2.5, 4.0, 10.0])
        self.assertAllClose(knp.digitize(x, bins), np.digitize(x, bins))
        self.assertAllClose(knp.Digitize()(x, bins), np.digitize(x, bins))
        self.assertTrue(
            standardize_dtype(knp.digitize(x, bins).dtype) == "int32"
        )
        self.assertTrue(
            standardize_dtype(knp.Digitize()(x, bins).dtype) == "int32"
        )

        x = np.array([1, 4, 10, 15])
        bins = np.array([4, 10, 14, 15])
        self.assertAllClose(knp.digitize(x, bins), np.digitize(x, bins))
        self.assertAllClose(knp.Digitize()(x, bins), np.digitize(x, bins))
        self.assertTrue(
            standardize_dtype(knp.digitize(x, bins).dtype) == "int32"
        )
        self.assertTrue(
            standardize_dtype(knp.Digitize()(x, bins).dtype) == "int32"
        )


class NumpyOneInputOpsCorrectnessTest(testing.TestCase, parameterized.TestCase):
    def test_mean(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.mean(x), np.mean(x))
        self.assertAllClose(knp.mean(x, axis=()), np.mean(x, axis=()))
        self.assertAllClose(knp.mean(x, axis=1), np.mean(x, axis=1))
        self.assertAllClose(knp.mean(x, axis=(1,)), np.mean(x, axis=(1,)))
        self.assertAllClose(
            knp.mean(x, axis=1, keepdims=True),
            np.mean(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Mean()(x), np.mean(x))
        self.assertAllClose(knp.Mean(axis=1)(x), np.mean(x, axis=1))
        self.assertAllClose(
            knp.Mean(axis=1, keepdims=True)(x),
            np.mean(x, axis=1, keepdims=True),
        )

        # test overflow
        x = np.array([65504, 65504, 65504], dtype="float16")
        self.assertAllClose(knp.mean(x), np.mean(x))

    @parameterized.product(
        axis=[None, (), 0, 1, 2, -1, -2, -3, (0, 1), (1, 2), (0, 2), (0, 1, 2)],
        keepdims=[True, False],
    )
    @pytest.mark.skipif(
        backend.backend() != "tensorflow",
        reason="IndexedSlices are only supported with TensorFlow backend.",
    )
    def test_mean_indexed_slices(self, axis, keepdims):
        import tensorflow as tf

        x = tf.IndexedSlices(
            [
                [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
                [[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]],
            ],
            (0, 2),
            (4, 2, 3),
        )
        x_np = tf.convert_to_tensor(x).numpy()
        self.assertAllClose(
            knp.mean(x, axis=axis, keepdims=keepdims),
            np.mean(x_np, axis=axis, keepdims=keepdims),
        )

        self.assertAllClose(
            knp.Mean(axis=axis, keepdims=keepdims)(x),
            np.mean(x_np, axis=axis, keepdims=keepdims),
        )

    def test_all(self):
        x = np.array([[True, False, True], [True, True, True]])
        self.assertAllClose(knp.all(x), np.all(x))
        self.assertAllClose(knp.all(x, axis=()), np.all(x, axis=()))
        self.assertAllClose(knp.all(x, axis=1), np.all(x, axis=1))
        self.assertAllClose(knp.all(x, axis=(1,)), np.all(x, axis=(1,)))
        self.assertAllClose(
            knp.all(x, axis=1, keepdims=True),
            np.all(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.All()(x), np.all(x))
        self.assertAllClose(knp.All(axis=1)(x), np.all(x, axis=1))
        self.assertAllClose(
            knp.All(axis=1, keepdims=True)(x),
            np.all(x, axis=1, keepdims=True),
        )

    def test_any(self):
        x = np.array([[True, False, True], [True, True, True]])
        self.assertAllClose(knp.any(x), np.any(x))
        self.assertAllClose(knp.any(x, axis=()), np.any(x, axis=()))
        self.assertAllClose(knp.any(x, axis=1), np.any(x, axis=1))
        self.assertAllClose(knp.any(x, axis=(1,)), np.any(x, axis=(1,)))
        self.assertAllClose(
            knp.any(x, axis=1, keepdims=True),
            np.any(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Any()(x), np.any(x))
        self.assertAllClose(knp.Any(axis=1)(x), np.any(x, axis=1))
        self.assertAllClose(
            knp.Any(axis=1, keepdims=True)(x),
            np.any(x, axis=1, keepdims=True),
        )

    def test_var(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.var(x), np.var(x))
        self.assertAllClose(knp.var(x, axis=()), np.var(x, axis=()))
        self.assertAllClose(knp.var(x, axis=1), np.var(x, axis=1))
        self.assertAllClose(knp.var(x, axis=(1,)), np.var(x, axis=(1,)))
        self.assertAllClose(
            knp.var(x, axis=1, keepdims=True),
            np.var(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Var()(x), np.var(x))
        self.assertAllClose(knp.Var(axis=1)(x), np.var(x, axis=1))
        self.assertAllClose(
            knp.Var(axis=1, keepdims=True)(x),
            np.var(x, axis=1, keepdims=True),
        )

    def test_sum(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.sum(x), np.sum(x))
        self.assertAllClose(knp.sum(x, axis=()), np.sum(x, axis=()))
        self.assertAllClose(knp.sum(x, axis=1), np.sum(x, axis=1))
        self.assertAllClose(knp.sum(x, axis=(1,)), np.sum(x, axis=(1,)))
        self.assertAllClose(
            knp.sum(x, axis=1, keepdims=True),
            np.sum(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Sum()(x), np.sum(x))
        self.assertAllClose(knp.Sum(axis=1)(x), np.sum(x, axis=1))
        self.assertAllClose(
            knp.Sum(axis=1, keepdims=True)(x),
            np.sum(x, axis=1, keepdims=True),
        )

    def test_amax(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.amax(x), np.amax(x))
        self.assertAllClose(knp.amax(x, axis=()), np.amax(x, axis=()))
        self.assertAllClose(knp.amax(x, axis=1), np.amax(x, axis=1))
        self.assertAllClose(knp.amax(x, axis=(1,)), np.amax(x, axis=(1,)))
        self.assertAllClose(
            knp.amax(x, axis=1, keepdims=True),
            np.amax(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Amax()(x), np.amax(x))
        self.assertAllClose(knp.Amax(axis=1)(x), np.amax(x, axis=1))
        self.assertAllClose(
            knp.Amax(axis=1, keepdims=True)(x),
            np.amax(x, axis=1, keepdims=True),
        )

    def test_amin(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.amin(x), np.amin(x))
        self.assertAllClose(knp.amin(x, axis=()), np.amin(x, axis=()))
        self.assertAllClose(knp.amin(x, axis=1), np.amin(x, axis=1))
        self.assertAllClose(knp.amin(x, axis=(1,)), np.amin(x, axis=(1,)))
        self.assertAllClose(
            knp.amin(x, axis=1, keepdims=True),
            np.amin(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Amin()(x), np.amin(x))
        self.assertAllClose(knp.Amin(axis=1)(x), np.amin(x, axis=1))
        self.assertAllClose(
            knp.Amin(axis=1, keepdims=True)(x),
            np.amin(x, axis=1, keepdims=True),
        )

    def test_square(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.square(x), np.square(x))

        self.assertAllClose(knp.Square()(x), np.square(x))

    def test_negative(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.negative(x), np.negative(x))

        self.assertAllClose(knp.Negative()(x), np.negative(x))

    def test_abs(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.abs(x), np.abs(x))

        self.assertAllClose(knp.Abs()(x), np.abs(x))

    def test_absolute(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.absolute(x), np.absolute(x))

        self.assertAllClose(knp.Absolute()(x), np.absolute(x))

    def test_squeeze(self):
        x = np.ones([1, 3, 1, 5])
        self.assertAllClose(knp.squeeze(x), np.squeeze(x))
        self.assertAllClose(knp.squeeze(x, axis=0), np.squeeze(x, axis=0))

        self.assertAllClose(knp.Squeeze()(x), np.squeeze(x))
        self.assertAllClose(knp.Squeeze(axis=0)(x), np.squeeze(x, axis=0))

    @pytest.mark.skipif(
        not backend.SUPPORTS_SPARSE_TENSORS,
        reason="Backend does not support sparse tensors.",
    )
    def test_squeeze_sparse(self):
        import tensorflow as tf

        x = tf.SparseTensor(
            indices=[[0, 0, 0, 0], [0, 2, 0, 4]],
            values=[1, 2],
            dense_shape=(1, 3, 1, 5),
        )
        x_np = tf.sparse.to_dense(x).numpy()
        self.assertAllClose(knp.squeeze(x), np.squeeze(x_np))
        self.assertAllClose(knp.squeeze(x, axis=0), np.squeeze(x_np, axis=0))

        self.assertAllClose(knp.Squeeze()(x), np.squeeze(x_np))
        self.assertAllClose(knp.Squeeze(axis=0)(x), np.squeeze(x_np, axis=0))

    def test_transpose(self):
        x = np.ones([1, 2, 3, 4, 5])
        self.assertAllClose(knp.transpose(x), np.transpose(x))
        self.assertAllClose(
            knp.transpose(x, axes=(1, 0, 3, 2, 4)),
            np.transpose(x, axes=(1, 0, 3, 2, 4)),
        )

        self.assertAllClose(knp.Transpose()(x), np.transpose(x))
        self.assertAllClose(
            knp.Transpose(axes=(1, 0, 3, 2, 4))(x),
            np.transpose(x, axes=(1, 0, 3, 2, 4)),
        )

    @pytest.mark.skipif(
        not backend.SUPPORTS_SPARSE_TENSORS,
        reason="Backend does not support sparse tensors.",
    )
    def test_transpose_sparse(self):
        import tensorflow as tf

        x = tf.SparseTensor(
            indices=[[0, 0, 0, 0, 0], [0, 1, 2, 3, 4]],
            values=[1, 2],
            dense_shape=(1, 2, 3, 4, 5),
        )
        x_np = tf.sparse.to_dense(x).numpy()

        self.assertIsInstance(knp.transpose(x), tf.SparseTensor)
        self.assertAllClose(knp.transpose(x), np.transpose(x_np))
        self.assertIsInstance(
            knp.transpose(x, axes=(1, 0, 3, 2, 4)), tf.SparseTensor
        )
        self.assertAllClose(
            knp.transpose(x, axes=(1, 0, 3, 2, 4)),
            np.transpose(x_np, axes=(1, 0, 3, 2, 4)),
        )

        self.assertIsInstance(knp.Transpose()(x), tf.SparseTensor)
        self.assertAllClose(knp.Transpose()(x), np.transpose(x_np))
        self.assertIsInstance(
            knp.Transpose(axes=(1, 0, 3, 2, 4))(x), tf.SparseTensor
        )
        self.assertAllClose(
            knp.Transpose(axes=(1, 0, 3, 2, 4))(x),
            np.transpose(x_np, axes=(1, 0, 3, 2, 4)),
        )

    def test_arccos(self):
        x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        self.assertAllClose(knp.arccos(x), np.arccos(x))

        self.assertAllClose(knp.Arccos()(x), np.arccos(x))

    def test_arccosh(self):
        x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        self.assertAllClose(knp.arccosh(x), np.arccosh(x))

        self.assertAllClose(knp.Arccosh()(x), np.arccosh(x))

    def test_arcsin(self):
        x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        self.assertAllClose(knp.arcsin(x), np.arcsin(x))

        self.assertAllClose(knp.Arcsin()(x), np.arcsin(x))

    def test_arcsinh(self):
        x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        self.assertAllClose(knp.arcsinh(x), np.arcsinh(x))

        self.assertAllClose(knp.Arcsinh()(x), np.arcsinh(x))

    def test_arctan(self):
        x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        self.assertAllClose(knp.arctan(x), np.arctan(x))

        self.assertAllClose(knp.Arctan()(x), np.arctan(x))

    def test_arctanh(self):
        x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        self.assertAllClose(knp.arctanh(x), np.arctanh(x))

        self.assertAllClose(knp.Arctanh()(x), np.arctanh(x))

    def test_argmax(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.argmax(x), np.argmax(x))
        self.assertAllClose(knp.argmax(x, axis=1), np.argmax(x, axis=1))

        self.assertAllClose(knp.Argmax()(x), np.argmax(x))
        self.assertAllClose(knp.Argmax(axis=1)(x), np.argmax(x, axis=1))

    def test_argmin(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.argmin(x), np.argmin(x))
        self.assertAllClose(knp.argmin(x, axis=1), np.argmin(x, axis=1))

        self.assertAllClose(knp.Argmin()(x), np.argmin(x))
        self.assertAllClose(knp.Argmin(axis=1)(x), np.argmin(x, axis=1))

    def test_argsort(self):
        x = np.array([[1, 2, 3], [4, 5, 6]])
        self.assertAllClose(knp.argsort(x), np.argsort(x))
        self.assertAllClose(knp.argsort(x, axis=1), np.argsort(x, axis=1))
        self.assertAllClose(knp.argsort(x, axis=None), np.argsort(x, axis=None))

        self.assertAllClose(knp.Argsort()(x), np.argsort(x))
        self.assertAllClose(knp.Argsort(axis=1)(x), np.argsort(x, axis=1))
        self.assertAllClose(knp.Argsort(axis=None)(x), np.argsort(x, axis=None))

    def test_array(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.array(x), np.array(x))
        self.assertAllClose(knp.Array()(x), np.array(x))
        self.assertTrue(backend.is_tensor(knp.array(x)))
        self.assertTrue(backend.is_tensor(knp.Array()(x)))

        # Check dtype convertion.
        x = [[1, 0, 1], [1, 1, 0]]
        output = knp.array(x, dtype="int32")
        self.assertEqual(standardize_dtype(output.dtype), "int32")
        x = [[1, 0, 1], [1, 1, 0]]
        output = knp.array(x, dtype="float32")
        self.assertEqual(standardize_dtype(output.dtype), "float32")
        x = [[1, 0, 1], [1, 1, 0]]
        output = knp.array(x, dtype="bool")
        self.assertEqual(standardize_dtype(output.dtype), "bool")

    def test_average(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        weights = np.ones([2, 3])
        weights_1d = np.ones([3])
        self.assertAllClose(knp.average(x), np.average(x))
        self.assertAllClose(knp.average(x, axis=()), np.average(x, axis=()))
        self.assertAllClose(knp.average(x, axis=1), np.average(x, axis=1))
        self.assertAllClose(knp.average(x, axis=(1,)), np.average(x, axis=(1,)))
        self.assertAllClose(
            knp.average(x, axis=1, weights=weights),
            np.average(x, axis=1, weights=weights),
        )
        self.assertAllClose(
            knp.average(x, axis=1, weights=weights_1d),
            np.average(x, axis=1, weights=weights_1d),
        )

        self.assertAllClose(knp.Average()(x), np.average(x))
        self.assertAllClose(knp.Average(axis=1)(x), np.average(x, axis=1))
        self.assertAllClose(
            knp.Average(axis=1)(x, weights=weights),
            np.average(x, axis=1, weights=weights),
        )
        self.assertAllClose(
            knp.Average(axis=1)(x, weights=weights_1d),
            np.average(x, axis=1, weights=weights_1d),
        )

    def test_bincount(self):
        if backend.backend() == "tensorflow":
            import tensorflow as tf

            if tf.test.is_gpu_available():
                self.skipTest("bincount does not work in tensorflow gpu")

        x = np.array([1, 1, 2, 3, 2, 4, 4, 5])
        weights = np.array([0, 0, 3, 2, 1, 1, 4, 2])
        minlength = 3
        self.assertAllClose(
            knp.bincount(x, weights=weights, minlength=minlength),
            np.bincount(x, weights=weights, minlength=minlength),
        )
        self.assertAllClose(
            knp.Bincount(weights=weights, minlength=minlength)(x),
            np.bincount(x, weights=weights, minlength=minlength),
        )
        x = np.array([[1, 1, 2, 3, 2, 4, 4, 5]])
        weights = np.array([[0, 0, 3, 2, 1, 1, 4, 2]])
        expected_output = np.array([[0, 0, 4, 2, 5, 2]])
        self.assertAllClose(
            knp.bincount(x, weights=weights, minlength=minlength),
            expected_output,
        )
        self.assertAllClose(
            knp.Bincount(weights=weights, minlength=minlength)(x),
            expected_output,
        )
        # test with weights=None
        expected_output = np.array([[0, 2, 2, 1, 2, 1]])
        self.assertAllClose(
            knp.Bincount(weights=None, minlength=minlength)(x),
            expected_output,
        )

    def test_broadcast_to(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(
            knp.broadcast_to(x, [2, 2, 3]),
            np.broadcast_to(x, [2, 2, 3]),
        )

        self.assertAllClose(
            knp.BroadcastTo([2, 2, 3])(x),
            np.broadcast_to(x, [2, 2, 3]),
        )

    def test_ceil(self):
        x = np.array([[1.2, 2.1, -2.5], [2.4, -11.9, -5.5]])
        self.assertAllClose(knp.ceil(x), np.ceil(x))
        self.assertAllClose(knp.Ceil()(x), np.ceil(x))

    def test_clip(self):
        x = np.array([[1.2, 2.1, -2.5], [2.4, -11.9, -5.5]])
        self.assertAllClose(knp.clip(x, -2, 2), np.clip(x, -2, 2))
        self.assertAllClose(knp.clip(x, -2, 2), np.clip(x, -2, 2))

        self.assertAllClose(knp.Clip(0, 1)(x), np.clip(x, 0, 1))
        self.assertAllClose(knp.Clip(0, 1)(x), np.clip(x, 0, 1))

    def test_concatenate(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [6, 5, 4]])
        z = np.array([[7, 8, 9], [9, 8, 7]])
        self.assertAllClose(
            knp.concatenate([x, y], axis=0),
            np.concatenate([x, y], axis=0),
        )
        self.assertAllClose(
            knp.concatenate([x, y, z], axis=0),
            np.concatenate([x, y, z], axis=0),
        )
        self.assertAllClose(
            knp.concatenate([x, y], axis=1),
            np.concatenate([x, y], axis=1),
        )

        self.assertAllClose(
            knp.Concatenate(axis=0)([x, y]),
            np.concatenate([x, y], axis=0),
        )
        self.assertAllClose(
            knp.Concatenate(axis=0)([x, y, z]),
            np.concatenate([x, y, z], axis=0),
        )
        self.assertAllClose(
            knp.Concatenate(axis=1)([x, y]),
            np.concatenate([x, y], axis=1),
        )

    @parameterized.named_parameters(
        [
            {"testcase_name": "axis_0", "axis": 0},
            {"testcase_name": "axis_1", "axis": 1},
        ]
    )
    @pytest.mark.skipif(
        not backend.SUPPORTS_SPARSE_TENSORS,
        reason="Backend does not support sparse tensors.",
    )
    def test_concatenate_sparse(self, axis):
        import tensorflow as tf

        x = tf.SparseTensor(
            indices=[[0, 0], [1, 2]], values=[1.0, 2.0], dense_shape=(2, 3)
        )
        x_np = tf.sparse.to_dense(x).numpy()

        y = tf.SparseTensor(
            indices=[[0, 0], [1, 1]], values=[4.0, 5.0], dense_shape=(2, 3)
        )
        y_np = tf.sparse.to_dense(y).numpy()
        z = np.random.rand(2, 3).astype("float32")

        self.assertAllClose(
            knp.concatenate([x, z], axis=axis),
            np.concatenate([x_np, z], axis=axis),
        )
        self.assertAllClose(
            knp.concatenate([z, x], axis=axis),
            np.concatenate([z, x_np], axis=axis),
        )
        self.assertAllClose(
            knp.concatenate([x, y], axis=axis),
            np.concatenate([x_np, y_np], axis=axis),
        )

        self.assertAllClose(
            knp.Concatenate(axis=axis)([x, z]),
            np.concatenate([x_np, z], axis=axis),
        )
        self.assertAllClose(
            knp.Concatenate(axis=axis)([z, x]),
            np.concatenate([z, x_np], axis=axis),
        )
        self.assertAllClose(
            knp.Concatenate(axis=axis)([x, y]),
            np.concatenate([x_np, y_np], axis=axis),
        )

        self.assertIsInstance(
            knp.concatenate([x, y], axis=axis), tf.SparseTensor
        )
        self.assertIsInstance(
            knp.Concatenate(axis=axis)([x, y]), tf.SparseTensor
        )

    def test_conjugate(self):
        x = np.array([[1 + 2j, 2 + 3j], [3 + 4j, 4 + 5j]])
        self.assertAllClose(knp.conjugate(x), np.conjugate(x))
        self.assertAllClose(knp.Conjugate()(x), np.conjugate(x))

    def test_conj(self):
        x = np.array([[1 + 2j, 2 + 3j], [3 + 4j, 4 + 5j]])
        self.assertAllClose(knp.conj(x), np.conj(x))
        self.assertAllClose(knp.Conj()(x), np.conj(x))

    def test_copy(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.copy(x), np.copy(x))
        self.assertAllClose(knp.Copy()(x), np.copy(x))

    def test_cos(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.cos(x), np.cos(x))
        self.assertAllClose(knp.Cos()(x), np.cos(x))

    def test_cosh(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.cosh(x), np.cosh(x))
        self.assertAllClose(knp.Cosh()(x), np.cosh(x))

    def test_count_nonzero(self):
        x = np.array([[0, 2, 3], [3, 2, 0]])
        self.assertAllClose(knp.count_nonzero(x), np.count_nonzero(x))
        self.assertAllClose(
            knp.count_nonzero(x, axis=()), np.count_nonzero(x, axis=())
        )
        self.assertAllClose(
            knp.count_nonzero(x, axis=1),
            np.count_nonzero(x, axis=1),
        )
        self.assertAllClose(
            knp.count_nonzero(x, axis=(1,)),
            np.count_nonzero(x, axis=(1,)),
        )

        self.assertAllClose(
            knp.CountNonzero()(x),
            np.count_nonzero(x),
        )
        self.assertAllClose(
            knp.CountNonzero(axis=1)(x),
            np.count_nonzero(x, axis=1),
        )

    @parameterized.product(
        axis=[None, 0, 1, -1],
        dtype=[None, "int32", "float32"],
    )
    def test_cumprod(self, axis, dtype):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(
            knp.cumprod(x, axis=axis, dtype=dtype),
            np.cumprod(x, axis=axis, dtype=dtype or x.dtype),
        )
        self.assertAllClose(
            knp.Cumprod(axis=axis, dtype=dtype)(x),
            np.cumprod(x, axis=axis, dtype=dtype or x.dtype),
        )

    @parameterized.product(
        axis=[None, 0, 1, -1],
        dtype=[None, "int32", "float32"],
    )
    def test_cumsum(self, axis, dtype):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(
            knp.cumsum(x, axis=axis, dtype=dtype),
            np.cumsum(x, axis=axis, dtype=dtype or x.dtype),
        )
        self.assertAllClose(
            knp.Cumsum(axis=axis, dtype=dtype)(x),
            np.cumsum(x, axis=axis, dtype=dtype or x.dtype),
        )

    def test_diag(self):
        x = np.array([1, 2, 3])
        self.assertAllClose(knp.diag(x), np.diag(x))
        self.assertAllClose(knp.diag(x, k=1), np.diag(x, k=1))
        self.assertAllClose(knp.diag(x, k=-1), np.diag(x, k=-1))

        self.assertAllClose(knp.Diag()(x), np.diag(x))
        self.assertAllClose(knp.Diag(k=1)(x), np.diag(x, k=1))
        self.assertAllClose(knp.Diag(k=-1)(x), np.diag(x, k=-1))

        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.diag(x), np.diag(x))
        self.assertAllClose(knp.diag(x, k=1), np.diag(x, k=1))
        self.assertAllClose(knp.diag(x, k=-1), np.diag(x, k=-1))

        self.assertAllClose(knp.Diag()(x), np.diag(x))
        self.assertAllClose(knp.Diag(k=1)(x), np.diag(x, k=1))
        self.assertAllClose(knp.Diag(k=-1)(x), np.diag(x, k=-1))

    def test_diagonal(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.diagonal(x), np.diagonal(x))
        self.assertAllClose(
            knp.diagonal(x, offset=1),
            np.diagonal(x, offset=1),
        )
        self.assertAllClose(
            knp.diagonal(x, offset=-1), np.diagonal(x, offset=-1)
        )

        self.assertAllClose(knp.Diagonal()(x), np.diagonal(x))
        self.assertAllClose(knp.Diagonal(offset=1)(x), np.diagonal(x, offset=1))
        self.assertAllClose(
            knp.Diagonal(offset=-1)(x), np.diagonal(x, offset=-1)
        )

        x = np.ones([2, 3, 4, 5])
        self.assertAllClose(knp.diagonal(x), np.diagonal(x))
        self.assertAllClose(
            knp.diagonal(x, offset=1, axis1=2, axis2=3),
            np.diagonal(x, offset=1, axis1=2, axis2=3),
        )
        self.assertAllClose(
            knp.diagonal(x, offset=-1, axis1=2, axis2=3),
            np.diagonal(x, offset=-1, axis1=2, axis2=3),
        )

    def test_diff(self):
        x = np.array([1, 2, 4, 7, 0])
        self.assertAllClose(knp.diff(x), np.diff(x))
        self.assertAllClose(knp.diff(x, n=2), np.diff(x, n=2))
        self.assertAllClose(knp.diff(x, n=3), np.diff(x, n=3))

        x = np.array([[1, 3, 6, 10], [0, 5, 6, 8]])
        self.assertAllClose(knp.diff(x), np.diff(x))
        self.assertAllClose(knp.diff(x, axis=0), np.diff(x, axis=0))
        self.assertAllClose(knp.diff(x, n=2, axis=0), np.diff(x, n=2, axis=0))
        self.assertAllClose(knp.diff(x, n=2, axis=1), np.diff(x, n=2, axis=1))

    def test_dot(self):
        x = np.arange(24).reshape([2, 3, 4]).astype("float32")
        y = np.arange(12).reshape([4, 3]).astype("float32")
        z = np.arange(4).astype("float32")
        self.assertAllClose(knp.dot(x, y), np.dot(x, y))
        self.assertAllClose(knp.dot(x, z), np.dot(x, z))
        self.assertAllClose(knp.dot(x, 2), np.dot(x, 2))

        self.assertAllClose(knp.Dot()(x, y), np.dot(x, y))
        self.assertAllClose(knp.Dot()(x, z), np.dot(x, z))
        self.assertAllClose(knp.Dot()(x, 2), np.dot(x, 2))

    def test_exp(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.exp(x), np.exp(x))
        self.assertAllClose(knp.Exp()(x), np.exp(x))

    def test_expand_dims(self):
        x = np.ones([2, 3, 4])
        self.assertAllClose(knp.expand_dims(x, 0), np.expand_dims(x, 0))
        self.assertAllClose(knp.expand_dims(x, 1), np.expand_dims(x, 1))
        self.assertAllClose(knp.expand_dims(x, -2), np.expand_dims(x, -2))

        self.assertAllClose(knp.ExpandDims(0)(x), np.expand_dims(x, 0))
        self.assertAllClose(knp.ExpandDims(1)(x), np.expand_dims(x, 1))
        self.assertAllClose(knp.ExpandDims(-2)(x), np.expand_dims(x, -2))

    @pytest.mark.skipif(
        not backend.SUPPORTS_SPARSE_TENSORS,
        reason="Backend does not support sparse tensors.",
    )
    def test_expand_dims_sparse(self):
        import tensorflow as tf

        x = tf.SparseTensor(
            indices=[[0, 0], [1, 2]],
            values=[1, 2],
            dense_shape=(2, 3),
        )
        x_np = tf.sparse.to_dense(x).numpy()
        self.assertAllClose(knp.expand_dims(x, 0), np.expand_dims(x_np, 0))
        self.assertAllClose(knp.expand_dims(x, 1), np.expand_dims(x_np, 1))
        self.assertAllClose(knp.expand_dims(x, -2), np.expand_dims(x_np, -2))

        self.assertAllClose(knp.ExpandDims(0)(x), np.expand_dims(x_np, 0))
        self.assertAllClose(knp.ExpandDims(1)(x), np.expand_dims(x_np, 1))
        self.assertAllClose(knp.ExpandDims(-2)(x), np.expand_dims(x_np, -2))

    def test_expm1(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.expm1(x), np.expm1(x))
        self.assertAllClose(knp.Expm1()(x), np.expm1(x))

    def test_flip(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.flip(x), np.flip(x))
        self.assertAllClose(knp.flip(x, 0), np.flip(x, 0))
        self.assertAllClose(knp.flip(x, 1), np.flip(x, 1))

        self.assertAllClose(knp.Flip()(x), np.flip(x))
        self.assertAllClose(knp.Flip(0)(x), np.flip(x, 0))
        self.assertAllClose(knp.Flip(1)(x), np.flip(x, 1))

    def test_floor(self):
        x = np.array([[1.1, 2.2, -3.3], [3.3, 2.2, -1.1]])
        self.assertAllClose(knp.floor(x), np.floor(x))
        self.assertAllClose(knp.Floor()(x), np.floor(x))

    def test_hstack(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [6, 5, 4]])
        self.assertAllClose(knp.hstack([x, y]), np.hstack([x, y]))
        self.assertAllClose(knp.Hstack()([x, y]), np.hstack([x, y]))

        x = np.ones([2, 3, 4])
        y = np.ones([2, 5, 4])
        self.assertAllClose(knp.hstack([x, y]), np.hstack([x, y]))
        self.assertAllClose(knp.Hstack()([x, y]), np.hstack([x, y]))

    def test_imag(self):
        x = np.array([[1 + 1j, 2 + 2j, 3 + 3j], [3 + 3j, 2 + 2j, 1 + 1j]])
        self.assertAllClose(knp.imag(x), np.imag(x))
        self.assertAllClose(knp.Imag()(x), np.imag(x))

    def test_isfinite(self):
        x = np.array([[1, 2, np.inf], [np.nan, np.nan, np.nan]])
        self.assertAllClose(knp.isfinite(x), np.isfinite(x))
        self.assertAllClose(knp.Isfinite()(x), np.isfinite(x))

    # TODO: fix and reenable
    def DISABLED_test_isinf(self):
        x = np.array([[1, 2, np.inf], [np.nan, np.nan, np.nan]])
        self.assertAllClose(knp.isinf(x), np.isinf(x))
        self.assertAllClose(knp.Isinf()(x), np.isinf(x))

    def test_isnan(self):
        x = np.array([[1, 2, np.inf], [np.nan, np.nan, np.nan]])
        self.assertAllClose(knp.isnan(x), np.isnan(x))
        self.assertAllClose(knp.Isnan()(x), np.isnan(x))

    def test_log(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.log(x), np.log(x))
        self.assertAllClose(knp.Log()(x), np.log(x))

    def test_log10(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.log10(x), np.log10(x))
        self.assertAllClose(knp.Log10()(x), np.log10(x))

    def test_log1p(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.log1p(x), np.log1p(x))
        self.assertAllClose(knp.Log1p()(x), np.log1p(x))

    def test_log2(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.log2(x), np.log2(x))
        self.assertAllClose(knp.Log2()(x), np.log2(x))

    def test_logaddexp(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.logaddexp(x, y), np.logaddexp(x, y))
        self.assertAllClose(knp.Logaddexp()(x, y), np.logaddexp(x, y))

    def test_logical_not(self):
        x = np.array([[True, False], [False, True]])
        self.assertAllClose(knp.logical_not(x), np.logical_not(x))
        self.assertAllClose(knp.LogicalNot()(x), np.logical_not(x))

    def test_max(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.max(x), np.max(x))
        self.assertAllClose(knp.Max()(x), np.max(x))

        self.assertAllClose(knp.max(x, 0), np.max(x, 0))
        self.assertAllClose(knp.Max(0)(x), np.max(x, 0))

        self.assertAllClose(knp.max(x, 1), np.max(x, 1))
        self.assertAllClose(knp.Max(1)(x), np.max(x, 1))

        # test max with initial
        self.assertAllClose(knp.max(x, initial=4), 4)

        # test empty tensor
        x = np.array([[]])
        self.assertAllClose(knp.max(x, initial=1), np.max(x, initial=1))
        self.assertAllClose(
            knp.max(x, initial=1, keepdims=True),
            np.max(x, initial=1, keepdims=True),
        )

    def test_min(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.min(x), np.min(x))
        self.assertAllClose(knp.Min()(x), np.min(x))

        self.assertAllClose(knp.min(x, 0), np.min(x, 0))
        self.assertAllClose(knp.Min(0)(x), np.min(x, 0))

        self.assertAllClose(knp.min(x, 1), np.min(x, 1))
        self.assertAllClose(knp.Min(1)(x), np.min(x, 1))

        # test min with initial
        self.assertAllClose(knp.min(x, initial=0), 0)

        # test empty tensor
        x = np.array([[]])
        self.assertAllClose(knp.min(x, initial=1), np.min(x, initial=1))
        self.assertAllClose(
            knp.min(x, initial=1, keepdims=True),
            np.min(x, initial=1, keepdims=True),
        )

    def test_median(self):
        x = np.array([[1, 2, 3], [3, 2, 1]]).astype("float32")
        self.assertAllClose(knp.median(x), np.median(x))
        self.assertAllClose(
            knp.median(x, keepdims=True), np.median(x, keepdims=True)
        )
        self.assertAllClose(knp.median(x, axis=1), np.median(x, axis=1))
        self.assertAllClose(knp.median(x, axis=(1,)), np.median(x, axis=(1,)))
        self.assertAllClose(
            knp.median(x, axis=1, keepdims=True),
            np.median(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Median()(x), np.median(x))
        self.assertAllClose(knp.Median(axis=1)(x), np.median(x, axis=1))
        self.assertAllClose(
            knp.Median(axis=1, keepdims=True)(x),
            np.median(x, axis=1, keepdims=True),
        )

    def test_meshgrid(self):
        x = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        z = np.array([7, 8, 9])
        self.assertAllClose(knp.meshgrid(x, y), np.meshgrid(x, y))
        self.assertAllClose(knp.meshgrid(x, z), np.meshgrid(x, z))
        self.assertAllClose(
            knp.meshgrid(x, y, z, indexing="ij"),
            np.meshgrid(x, y, z, indexing="ij"),
        )
        self.assertAllClose(knp.Meshgrid()(x, y), np.meshgrid(x, y))
        self.assertAllClose(knp.Meshgrid()(x, z), np.meshgrid(x, z))
        self.assertAllClose(
            knp.Meshgrid(indexing="ij")(x, y, z),
            np.meshgrid(x, y, z, indexing="ij"),
        )

        if backend.backend() == "tensorflow":
            # Arguments to `jax.numpy.meshgrid` must be 1D now.
            x = np.ones([1, 2, 3])
            y = np.ones([4, 5, 6, 6])
            z = np.ones([7, 8])
            self.assertAllClose(knp.meshgrid(x, y), np.meshgrid(x, y))
            self.assertAllClose(knp.meshgrid(x, z), np.meshgrid(x, z))
            self.assertAllClose(
                knp.meshgrid(x, y, z, indexing="ij"),
                np.meshgrid(x, y, z, indexing="ij"),
            )
            self.assertAllClose(knp.Meshgrid()(x, y), np.meshgrid(x, y))
            self.assertAllClose(knp.Meshgrid()(x, z), np.meshgrid(x, z))
            self.assertAllClose(
                knp.Meshgrid(indexing="ij")(x, y, z),
                np.meshgrid(x, y, z, indexing="ij"),
            )

    def test_moveaxis(self):
        x = np.array([[[0, 1], [2, 3]], [[4, 5], [6, 7]]])
        self.assertAllClose(knp.moveaxis(x, 0, -1), np.moveaxis(x, 0, -1))
        self.assertAllClose(knp.moveaxis(x, -1, 0), np.moveaxis(x, -1, 0))
        self.assertAllClose(
            knp.moveaxis(x, (0, 1), (1, 0)),
            np.moveaxis(x, (0, 1), (1, 0)),
        )
        self.assertAllClose(
            knp.moveaxis(x, [0, 1, 2], [2, 0, 1]),
            np.moveaxis(x, [0, 1, 2], [2, 0, 1]),
        )
        self.assertAllClose(knp.Moveaxis(-1, 0)(x), np.moveaxis(x, -1, 0))
        self.assertAllClose(
            knp.Moveaxis((0, 1), (1, 0))(x),
            np.moveaxis(x, (0, 1), (1, 0)),
        )

        self.assertAllClose(
            knp.Moveaxis([0, 1, 2], [2, 0, 1])(x),
            np.moveaxis(x, [0, 1, 2], [2, 0, 1]),
        )

    def test_ndim(self):
        x = np.array([1, 2, 3])
        self.assertEqual(knp.ndim(x), np.ndim(x))
        self.assertEqual(knp.Ndim()(x), np.ndim(x))

    def test_nonzero(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.nonzero(x), np.nonzero(x))
        self.assertAllClose(knp.Nonzero()(x), np.nonzero(x))

    def test_ones_like(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.ones_like(x), np.ones_like(x))
        self.assertAllClose(knp.OnesLike()(x), np.ones_like(x))

    @parameterized.named_parameters(
        named_product(
            dtype=[
                "float16",
                "float32",
                "float64",
                "uint8",
                "int8",
                "int16",
                "int32",
            ],
            mode=["constant", "reflect", "symmetric"],
            constant_values=[None, 0, 2],
        )
    )
    def test_pad(self, dtype, mode, constant_values):
        # 2D
        x = np.ones([2, 3], dtype=dtype)
        pad_width = ((1, 1), (1, 1))

        if mode != "constant":
            if constant_values is not None:
                with self.assertRaisesRegex(
                    ValueError,
                    "Argument `constant_values` can only be "
                    "provided when `mode == 'constant'`",
                ):
                    knp.pad(
                        x, pad_width, mode=mode, constant_values=constant_values
                    )
                return
            # constant_values is None
            kwargs = {}
        else:
            # mode is constant
            kwargs = {"constant_values": constant_values or 0}

        self.assertAllClose(
            knp.pad(x, pad_width, mode=mode, constant_values=constant_values),
            np.pad(x, pad_width, mode=mode, **kwargs),
        )
        self.assertAllClose(
            knp.Pad(pad_width, mode=mode)(x, constant_values=constant_values),
            np.pad(x, pad_width, mode=mode, **kwargs),
        )

        # 5D (pad last 3D)
        x = np.ones([2, 3, 4, 5, 6], dtype=dtype)
        pad_width = ((0, 0), (0, 0), (2, 3), (1, 1), (1, 1))
        self.assertAllClose(
            knp.pad(x, pad_width, mode=mode, constant_values=constant_values),
            np.pad(x, pad_width, mode=mode, **kwargs),
        )
        self.assertAllClose(
            knp.Pad(pad_width, mode=mode)(x, constant_values=constant_values),
            np.pad(x, pad_width, mode=mode, **kwargs),
        )

        # 5D (pad arbitrary dimensions)
        if backend.backend() == "torch" and mode != "constant":
            self.skipTest(
                "reflect and symmetric padding for arbitary dimensions are not "
                "supported by torch"
            )
        x = np.ones([2, 3, 4, 5, 6], dtype=dtype)
        pad_width = ((1, 1), (2, 1), (3, 2), (4, 3), (5, 4))
        self.assertAllClose(
            knp.pad(x, pad_width, mode=mode, constant_values=constant_values),
            np.pad(x, pad_width, mode=mode, **kwargs),
        )
        self.assertAllClose(
            knp.Pad(pad_width, mode=mode)(x, constant_values=constant_values),
            np.pad(x, pad_width, mode=mode, **kwargs),
        )

    def test_prod(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.prod(x), np.prod(x))
        self.assertAllClose(knp.prod(x, axis=()), np.prod(x, axis=()))
        self.assertAllClose(knp.prod(x, axis=1), np.prod(x, axis=1))
        self.assertAllClose(knp.prod(x, axis=(1,)), np.prod(x, axis=(1,)))
        self.assertAllClose(
            knp.prod(x, axis=1, keepdims=True),
            np.prod(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Prod()(x), np.prod(x))
        self.assertAllClose(knp.Prod(axis=1)(x), np.prod(x, axis=1))
        self.assertAllClose(
            knp.Prod(axis=1, keepdims=True)(x),
            np.prod(x, axis=1, keepdims=True),
        )

    def test_ravel(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.ravel(x), np.ravel(x))
        self.assertAllClose(knp.Ravel()(x), np.ravel(x))

    def test_real(self):
        x = np.array([[1, 2, 3 - 3j], [3, 2, 1 + 5j]])
        self.assertAllClose(knp.real(x), np.real(x))
        self.assertAllClose(knp.Real()(x), np.real(x))

    def test_reciprocal(self):
        x = np.array([[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]])
        self.assertAllClose(knp.reciprocal(x), np.reciprocal(x))
        self.assertAllClose(knp.Reciprocal()(x), np.reciprocal(x))

    def test_repeat(self):
        x = np.array([[1, 2], [3, 4]])
        self.assertAllClose(knp.repeat(x, 2), np.repeat(x, 2))
        self.assertAllClose(knp.repeat(x, 3, axis=1), np.repeat(x, 3, axis=1))
        self.assertAllClose(
            knp.repeat(x, np.array([1, 2]), axis=-1),
            np.repeat(x, np.array([1, 2]), axis=-1),
        )
        self.assertAllClose(knp.Repeat(2)(x), np.repeat(x, 2))
        self.assertAllClose(knp.Repeat(3, axis=1)(x), np.repeat(x, 3, axis=1))
        self.assertAllClose(
            knp.Repeat(np.array([1, 2]), axis=0)(x),
            np.repeat(x, np.array([1, 2]), axis=0),
        )

    def test_reshape(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.reshape(x, [3, 2]), np.reshape(x, [3, 2]))
        self.assertAllClose(knp.Reshape([3, 2])(x), np.reshape(x, [3, 2]))
        self.assertAllClose(knp.Reshape(-1)(x), np.reshape(x, -1))

    @pytest.mark.skipif(
        not backend.SUPPORTS_SPARSE_TENSORS,
        reason="Backend does not support sparse tensors.",
    )
    def test_reshape_sparse(self):
        import tensorflow as tf

        x = tf.SparseTensor(
            indices=[[0, 0], [1, 2]],
            values=[1, 2],
            dense_shape=(2, 3),
        )
        x_np = tf.sparse.to_dense(x).numpy()
        self.assertIsInstance(knp.reshape(x, [3, 2]), tf.SparseTensor)
        self.assertAllClose(knp.reshape(x, [3, 2]), np.reshape(x_np, [3, 2]))
        self.assertIsInstance(knp.Reshape([3, 2])(x), tf.SparseTensor)
        self.assertAllClose(knp.Reshape([3, 2])(x), np.reshape(x_np, [3, 2]))

    def test_roll(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.roll(x, 1), np.roll(x, 1))
        self.assertAllClose(knp.roll(x, 1, axis=1), np.roll(x, 1, axis=1))
        self.assertAllClose(knp.roll(x, -1, axis=0), np.roll(x, -1, axis=0))
        self.assertAllClose(knp.Roll(1)(x), np.roll(x, 1))
        self.assertAllClose(knp.Roll(1, axis=1)(x), np.roll(x, 1, axis=1))
        self.assertAllClose(knp.Roll(-1, axis=0)(x), np.roll(x, -1, axis=0))

    def test_round(self):
        x = np.array([[1.1, 2.5, 3.9], [3.2, 2.3, 1.8]])
        self.assertAllClose(knp.round(x), np.round(x))
        self.assertAllClose(knp.Round()(x), np.round(x))

    def test_sign(self):
        x = np.array([[1, -2, 3], [-3, 2, -1]])
        self.assertAllClose(knp.sign(x), np.sign(x))
        self.assertAllClose(knp.Sign()(x), np.sign(x))

    def test_sin(self):
        x = np.array([[1, -2, 3], [-3, 2, -1]])
        self.assertAllClose(knp.sin(x), np.sin(x))
        self.assertAllClose(knp.Sin()(x), np.sin(x))

    def test_sinh(self):
        x = np.array([[1, -2, 3], [-3, 2, -1]])
        self.assertAllClose(knp.sinh(x), np.sinh(x))
        self.assertAllClose(knp.Sinh()(x), np.sinh(x))

    def test_size(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.size(x), np.size(x))
        self.assertAllClose(knp.Size()(x), np.size(x))

    def test_sort(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.sort(x), np.sort(x))
        self.assertAllClose(knp.Sort()(x), np.sort(x))
        self.assertAllClose(knp.sort(x, axis=0), np.sort(x, axis=0))
        self.assertAllClose(knp.Sort(axis=0)(x), np.sort(x, axis=0))

    def test_split(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.split(x, 2), np.split(x, 2))
        self.assertAllClose(knp.Split(2)(x), np.split(x, 2))
        self.assertAllClose(
            knp.split(x, [1, 2], axis=1),
            np.split(x, [1, 2], axis=1),
        )
        self.assertAllClose(
            knp.Split([1, 2], axis=1)(x),
            np.split(x, [1, 2], axis=1),
        )

        # test invalid indices_or_sections
        with self.assertRaises(Exception):
            knp.split(x, 3)

        # test zero dimension
        x = np.ones(shape=(0,))
        self.assertEqual(len(knp.split(x, 2)), 2)
        self.assertEqual(len(knp.Split(2)(x)), 2)

    def test_sqrt(self):
        x = np.array([[1, 4, 9], [16, 25, 36]], dtype="float32")
        ref_y = np.sqrt(x)
        y = knp.sqrt(x)
        self.assertEqual(standardize_dtype(y.dtype), "float32")
        self.assertAllClose(y, ref_y)
        y = knp.Sqrt()(x)
        self.assertEqual(standardize_dtype(y.dtype), "float32")
        self.assertAllClose(y, ref_y)

    @pytest.mark.skipif(
        backend.backend() == "jax", reason="JAX does not support float64."
    )
    def test_sqrt_float64(self):
        x = np.array([[1, 4, 9], [16, 25, 36]], dtype="float64")
        ref_y = np.sqrt(x)
        y = knp.sqrt(x)
        self.assertEqual(standardize_dtype(y.dtype), "float64")
        self.assertAllClose(y, ref_y)
        y = knp.Sqrt()(x)
        self.assertEqual(standardize_dtype(y.dtype), "float64")
        self.assertAllClose(y, ref_y)

    def test_sqrt_int32(self):
        x = np.array([[1, 4, 9], [16, 25, 36]], dtype="int32")
        ref_y = np.sqrt(x)
        y = knp.sqrt(x)
        self.assertEqual(standardize_dtype(y.dtype), "float32")
        self.assertAllClose(y, ref_y)
        y = knp.Sqrt()(x)
        self.assertEqual(standardize_dtype(y.dtype), "float32")
        self.assertAllClose(y, ref_y)

    def test_stack(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [6, 5, 4]])
        self.assertAllClose(knp.stack([x, y]), np.stack([x, y]))
        self.assertAllClose(knp.stack([x, y], axis=1), np.stack([x, y], axis=1))
        self.assertAllClose(knp.Stack()([x, y]), np.stack([x, y]))
        self.assertAllClose(knp.Stack(axis=1)([x, y]), np.stack([x, y], axis=1))

    def test_std(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.std(x), np.std(x))
        self.assertAllClose(knp.std(x, axis=1), np.std(x, axis=1))
        self.assertAllClose(
            knp.std(x, axis=1, keepdims=True),
            np.std(x, axis=1, keepdims=True),
        )

        self.assertAllClose(knp.Std()(x), np.std(x))
        self.assertAllClose(knp.Std(axis=1)(x), np.std(x, axis=1))
        self.assertAllClose(
            knp.Std(axis=1, keepdims=True)(x),
            np.std(x, axis=1, keepdims=True),
        )

    def test_swapaxes(self):
        x = np.arange(24).reshape([1, 2, 3, 4])
        self.assertAllClose(
            knp.swapaxes(x, 0, 1),
            np.swapaxes(x, 0, 1),
        )
        self.assertAllClose(
            knp.Swapaxes(0, 1)(x),
            np.swapaxes(x, 0, 1),
        )

    def test_tan(self):
        x = np.array([[1, -2, 3], [-3, 2, -1]])
        self.assertAllClose(knp.tan(x), np.tan(x))
        self.assertAllClose(knp.Tan()(x), np.tan(x))

    def test_tanh(self):
        x = np.array([[1, -2, 3], [-3, 2, -1]])
        self.assertAllClose(knp.tanh(x), np.tanh(x))
        self.assertAllClose(knp.Tanh()(x), np.tanh(x))

    def test_tile(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        self.assertAllClose(knp.tile(x, [2, 3]), np.tile(x, [2, 3]))
        self.assertAllClose(knp.Tile([2, 3])(x), np.tile(x, [2, 3]))

    def test_trace(self):
        x = np.arange(24).reshape([1, 2, 3, 4])
        self.assertAllClose(knp.trace(x), np.trace(x))
        self.assertAllClose(
            knp.trace(x, axis1=2, axis2=3),
            np.trace(x, axis1=2, axis2=3),
        )
        self.assertAllClose(
            knp.Trace(axis1=2, axis2=3)(x),
            np.trace(x, axis1=2, axis2=3),
        )

    def test_tril(self):
        x = np.arange(24).reshape([1, 2, 3, 4])
        self.assertAllClose(knp.tril(x), np.tril(x))
        self.assertAllClose(knp.tril(x, -1), np.tril(x, -1))
        self.assertAllClose(knp.Tril(-1)(x), np.tril(x, -1))

    def test_triu(self):
        x = np.arange(24).reshape([1, 2, 3, 4])
        self.assertAllClose(knp.triu(x), np.triu(x))
        self.assertAllClose(knp.triu(x, -1), np.triu(x, -1))
        self.assertAllClose(knp.Triu(-1)(x), np.triu(x, -1))

    def test_vstack(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [6, 5, 4]])
        self.assertAllClose(knp.vstack([x, y]), np.vstack([x, y]))
        self.assertAllClose(knp.Vstack()([x, y]), np.vstack([x, y]))

    def test_floordiv(self):
        x = np.array([[1, 2, 3], [3, 2, 1]])
        y = np.array([[4, 5, 6], [3, 2, 1]])
        z = np.array([[[1, 2, 3], [3, 2, 1]]])
        self.assertAllClose(knp.floor_divide(x, y), np.floor_divide(x, y))
        self.assertAllClose(knp.floor_divide(x, z), np.floor_divide(x, z))

        self.assertAllClose(knp.FloorDivide()(x, y), np.floor_divide(x, y))
        self.assertAllClose(knp.FloorDivide()(x, z), np.floor_divide(x, z))

    def test_xor(self):
        x = np.array([[True, False], [True, True]])
        y = np.array([[False, False], [True, False]])
        self.assertAllClose(knp.logical_xor(x, y), np.logical_xor(x, y))
        self.assertAllClose(knp.logical_xor(x, True), np.logical_xor(x, True))
        self.assertAllClose(knp.logical_xor(True, x), np.logical_xor(True, x))

        self.assertAllClose(knp.LogicalXor()(x, y), np.logical_xor(x, y))
        self.assertAllClose(knp.LogicalXor()(x, True), np.logical_xor(x, True))
        self.assertAllClose(knp.LogicalXor()(True, x), np.logical_xor(True, x))


class NumpyArrayCreateOpsCorrectnessTest(testing.TestCase):
    def test_ones(self):
        self.assertAllClose(knp.ones([2, 3]), np.ones([2, 3]))
        self.assertAllClose(knp.Ones()([2, 3]), np.ones([2, 3]))

    def test_zeros(self):
        self.assertAllClose(knp.zeros([2, 3]), np.zeros([2, 3]))
        self.assertAllClose(knp.Zeros()([2, 3]), np.zeros([2, 3]))

    def test_eye(self):
        self.assertAllClose(knp.eye(3), np.eye(3))
        self.assertAllClose(knp.eye(3, 4), np.eye(3, 4))
        self.assertAllClose(knp.eye(3, 4, 1), np.eye(3, 4, 1))

        self.assertAllClose(knp.Eye()(3), np.eye(3))
        self.assertAllClose(knp.Eye()(3, 4), np.eye(3, 4))
        self.assertAllClose(knp.Eye()(3, 4, 1), np.eye(3, 4, 1))

    def test_arange(self):
        self.assertAllClose(knp.arange(3), np.arange(3))
        self.assertAllClose(knp.arange(3, 7), np.arange(3, 7))
        self.assertAllClose(knp.arange(3, 7, 2), np.arange(3, 7, 2))

        self.assertAllClose(knp.Arange()(3), np.arange(3))
        self.assertAllClose(knp.Arange()(3, 7), np.arange(3, 7))
        self.assertAllClose(knp.Arange()(3, 7, 2), np.arange(3, 7, 2))

        self.assertEqual(standardize_dtype(knp.arange(3).dtype), "int32")
        with pytest.warns(None) as record:
            knp.arange(3, dtype="int")
        self.assertEqual(len(record), 0)

    def test_full(self):
        self.assertAllClose(knp.full([2, 3], 0), np.full([2, 3], 0))
        self.assertAllClose(knp.full([2, 3], 0.1), np.full([2, 3], 0.1))
        self.assertAllClose(
            knp.full([2, 3], np.array([1, 4, 5])),
            np.full([2, 3], np.array([1, 4, 5])),
        )

        self.assertAllClose(knp.Full()([2, 3], 0), np.full([2, 3], 0))
        self.assertAllClose(knp.Full()([2, 3], 0.1), np.full([2, 3], 0.1))
        self.assertAllClose(
            knp.Full()([2, 3], np.array([1, 4, 5])),
            np.full([2, 3], np.array([1, 4, 5])),
        )

    def test_identity(self):
        self.assertAllClose(knp.identity(3), np.identity(3))
        self.assertAllClose(knp.Identity()(3), np.identity(3))

    def test_tri(self):
        self.assertAllClose(knp.tri(3), np.tri(3))
        self.assertAllClose(knp.tri(3, 4), np.tri(3, 4))
        self.assertAllClose(knp.tri(3, 4, 1), np.tri(3, 4, 1))

        self.assertAllClose(knp.Tri()(3), np.tri(3))
        self.assertAllClose(knp.Tri()(3, 4), np.tri(3, 4))
        self.assertAllClose(knp.Tri()(3, 4, 1), np.tri(3, 4, 1))


def create_sparse_tensor(x, indices_from=None, start=0, delta=2):
    if indices_from is not None:
        indices = indices_from.indices
    else:
        flat_indices = np.arange(start, x.size, delta)
        indices = np.stack(np.where(np.ones_like(x)), axis=1)[flat_indices]

    if backend.backend() == "tensorflow":
        import tensorflow as tf

        return tf.SparseTensor(indices, tf.gather_nd(x, indices), x.shape)


def create_indexed_slices(x, indices_from=None, start=0, delta=2):
    indices = np.arange(start, x.shape[0], delta)

    if backend.backend() == "tensorflow":
        import tensorflow as tf

        if indices_from is not None:
            indices = indices_from.indices
        return tf.IndexedSlices(tf.gather(x, indices), indices, x.shape)


def get_sparseness_combinations(sparsify_fn):
    x = np.array([[1, 2, 3], [3, 2, 1]])
    y = np.array([[4, 5, 6], [3, 2, 1]])
    scalar = backend.convert_to_tensor(2)
    x_sp = sparsify_fn(x)
    y_sp = sparsify_fn(y, indices_from=x_sp)
    x_sp_sup = sparsify_fn(x, start=0, delta=1)
    y_sp_dis = sparsify_fn(y, start=1)
    y_sp_sup = sparsify_fn(y, start=0, delta=1)
    x = backend.convert_to_tensor(x)
    y = backend.convert_to_tensor(y)
    return [
        {"testcase_name": "sparse_dense", "x": x_sp, "y": y},
        {"testcase_name": "dense_sparse", "x": x, "y": y_sp},
        {"testcase_name": "sparse_scalar", "x": x_sp, "y": scalar},
        {"testcase_name": "scalar_sparse", "x": scalar, "y": y_sp},
        {"testcase_name": "sparse_sparse_same", "x": x_sp, "y": y_sp},
        {"testcase_name": "sparse_sparse_disjoint", "x": x_sp, "y": y_sp_dis},
        {"testcase_name": "sparse_sparse_superset", "x": x_sp, "y": y_sp_sup},
        {"testcase_name": "sparse_sparse_subset", "x": x_sp_sup, "y": y_sp},
    ]


def sparseness(x):
    if isinstance(x, KerasTensor):
        return "sparse" if x.sparse else "dense"
    elif x.__class__.__name__ == "SparseTensor":
        return "sparse"
    elif x.__class__.__name__ == "IndexedSlices":
        return "slices"
    elif not hasattr(x, "shape") or not x.shape:
        return "scalar"
    else:
        return "dense"


def union_sparseness(x1, x2):
    x1_sparseness = sparseness(x1)
    x2_sparseness = sparseness(x2)
    if any(s in ("scalar", "dense") for s in (x1_sparseness, x2_sparseness)):
        return "dense"
    if x1_sparseness != x2_sparseness:
        raise ValueError(f"Illegal combination of operands: {x1} {x2}")
    return x1_sparseness


def intersection_sparseness(x1, x2):
    x1_sparseness = sparseness(x1)
    x2_sparseness = sparseness(x2)
    if x1_sparseness == "scalar":
        return x2_sparseness
    if x2_sparseness in ("scalar", "dense"):
        return x1_sparseness
    if x1_sparseness == "dense":
        return x2_sparseness
    if x1_sparseness != x2_sparseness:
        raise ValueError(f"Illegal combination of operands: {x1} {x2}")
    return x1_sparseness


def division_sparseness(x1, x2):
    x1_sparseness = sparseness(x1)
    x2_sparseness = sparseness(x2)
    if x2_sparseness in ("sparse", "slices"):
        return "dense"
    return "dense" if x1_sparseness == "scalar" else x1_sparseness


@pytest.mark.skipif(
    not backend.SUPPORTS_SPARSE_TENSORS,
    reason="Backend does not support sparse tensors.",
)
class SparseTest(testing.TestCase, parameterized.TestCase):
    DTYPES = ["int32", "float32"]
    DENSIFYING_UNARY_OPS = [
        "arccos",
        "arccosh",
        "cos",
        "cosh",
        "exp",
        "log",
        "log10",
        "log2",
        "reciprocal",
    ]
    DENSIFYING_UNARY_OPS_TESTS = [
        {
            "testcase_name": op,
            "op_function": getattr(knp, op),
            "op_class": getattr(knp, op.capitalize()),
            "np_op": getattr(np, op),
        }
        for op in DENSIFYING_UNARY_OPS
    ]
    UNARY_OPS = [
        "abs",
        "absolute",
        "arcsin",
        "arcsinh",
        "arctan",
        "arctanh",
        "ceil",
        "conj",
        "conjugate",
        "copy",
        "expm1",
        "floor",
        "imag",
        "log1p",
        "negative",
        "real",
        "round",
        "sign",
        "sin",
        "sinh",
        "sqrt",
        "square",
        "tan",
        "tanh",
    ]
    UNARY_OPS_TESTS = [
        {
            "testcase_name": op,
            "op_function": getattr(knp, op),
            "op_class": getattr(knp, op.capitalize()),
            "np_op": getattr(np, op),
        }
        for op in UNARY_OPS
    ]

    BINARY_OPS = [
        ("add", union_sparseness),
        ("subtract", union_sparseness),
        ("maximum", union_sparseness),
        ("minimum", union_sparseness),
        ("multiply", intersection_sparseness),
        ("mod", division_sparseness),
        ("divide", division_sparseness),
        ("true_divide", division_sparseness),
        ("floor_divide", division_sparseness),
    ]
    BINARY_OPS_TESTS = [
        {
            "testcase_name": op,
            "op_function": getattr(knp, op),
            "op_class": getattr(
                knp, "".join(w.capitalize() for w in op.split("_"))
            ),
            "np_op": getattr(np, op),
            "op_sparseness": op_sparseness,
        }
        for op, op_sparseness in BINARY_OPS
    ]

    def assertSameSparseness(self, x, y):
        self.assertEquals(sparseness(x), sparseness(y))

    def assertSparseness(self, x, expected_sparseness):
        self.assertEquals(sparseness(x), expected_sparseness)

    @parameterized.named_parameters(UNARY_OPS_TESTS)
    def test_unary_symbolic_static_shape(self, op_function, op_class, np_op):
        x = KerasTensor([2, 3], sparse=True)
        self.assertEqual(op_function(x).shape, (2, 3))
        self.assertTrue(op_function(x).sparse)
        self.assertEqual(op_class()(x).shape, (2, 3))
        self.assertTrue(op_class()(x).sparse)

    @parameterized.named_parameters(UNARY_OPS_TESTS)
    def test_unary_symbolic_dynamic_shape(self, op_function, op_class, np_op):
        x = KerasTensor([None, 3], sparse=True)
        self.assertEqual(op_function(x).shape, (None, 3))
        self.assertTrue(op_function(x).sparse)
        self.assertEqual(op_class()(x).shape, (None, 3))
        self.assertTrue(op_class()(x).sparse)

    @parameterized.named_parameters(DENSIFYING_UNARY_OPS_TESTS)
    def test_densifying_unary_sparse_correctness(
        self, op_function, op_class, np_op
    ):
        x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        x = create_sparse_tensor(x)
        x_np = backend.convert_to_numpy(x)

        self.assertAllClose(op_function(x), np_op(x_np))
        self.assertAllClose(op_class()(x), np_op(x_np))

    @parameterized.named_parameters(DENSIFYING_UNARY_OPS_TESTS)
    def test_densifying_unary_indexed_slices_correctness(
        self, op_function, op_class, np_op
    ):
        x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        x = create_indexed_slices(x)
        x_np = backend.convert_to_numpy(x)

        self.assertAllClose(op_function(x), np_op(x_np))
        self.assertAllClose(op_class()(x), np_op(x_np))

    @parameterized.named_parameters(UNARY_OPS_TESTS)
    def test_unary_sparse_correctness(self, op_function, op_class, np_op):
        if op_function.__name__ in ("conj", "conjugate", "imag", "real"):
            x = np.array([[1 + 1j, 2 + 2j, 3 + 3j], [3 + 3j, 2 + 2j, 1 + 1j]])
        else:
            x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        x = create_sparse_tensor(x)
        x_np = backend.convert_to_numpy(x)

        self.assertAllClose(op_function(x), np_op(x_np))
        self.assertSameSparseness(op_function(x), x)
        self.assertAllClose(op_class()(x), np_op(x_np))
        self.assertSameSparseness(op_class()(x), x)

    @parameterized.named_parameters(UNARY_OPS_TESTS)
    def test_unary_indexed_slices_correctness(
        self, op_function, op_class, np_op
    ):
        if op_function.__name__ in ("conj", "conjugate", "imag", "real"):
            x = np.array([[1 + 1j, 2 + 2j, 3 + 3j], [3 + 3j, 2 + 2j, 1 + 1j]])
        else:
            x = np.array([[1, 0.5, -0.7], [0.9, 0.2, -1]])
        x = create_indexed_slices(x)
        x_np = backend.convert_to_numpy(x)

        self.assertAllClose(op_function(x), np_op(x_np))
        self.assertSameSparseness(op_function(x), x)
        self.assertAllClose(op_class()(x), np_op(x_np))
        self.assertSameSparseness(op_class()(x), x)

    @parameterized.named_parameters(
        named_product(
            BINARY_OPS_TESTS, x_sparse=[True, False], y_sparse=[True, False]
        )
    )
    def test_binary_symbolic_static_shape(
        self, x_sparse, y_sparse, op_function, op_class, np_op, op_sparseness
    ):
        x = KerasTensor([2, 3], sparse=x_sparse)
        y = KerasTensor([2, 3], sparse=y_sparse)
        self.assertEqual(op_function(x, y).shape, (2, 3))
        self.assertSparseness(op_function(x, y), op_sparseness(x, y))
        self.assertEqual(op_class()(x, y).shape, (2, 3))
        self.assertSparseness(op_class()(x, y), op_sparseness(x, y))

    @parameterized.named_parameters(
        named_product(
            BINARY_OPS_TESTS, x_sparse=[True, False], y_sparse=[True, False]
        )
    )
    def test_binary_symbolic_dynamic_shape(
        self, x_sparse, y_sparse, op_function, op_class, np_op, op_sparseness
    ):
        x = KerasTensor([None, 3], sparse=x_sparse)
        y = KerasTensor([2, None], sparse=y_sparse)
        self.assertEqual(op_function(x, y).shape, (2, 3))
        self.assertSparseness(op_function(x, y), op_sparseness(x, y))
        self.assertEqual(op_class()(x, y).shape, (2, 3))
        self.assertSparseness(op_class()(x, y), op_sparseness(x, y))

    @parameterized.named_parameters(
        named_product(
            BINARY_OPS_TESTS,
            get_sparseness_combinations(create_sparse_tensor),
            dtype=DTYPES,
        )
    )
    def test_binary_correctness_sparse_tensor(
        self, x, y, op_function, op_class, np_op, op_sparseness, dtype
    ):
        if dtype == "int32" and op_function.__name__ in ("floor_divide", "mod"):
            self.skipTest(f"{op_function.__name__} does not support integers")

        x = backend.cast(x, dtype)
        y = backend.cast(y, dtype)
        expected_result = np_op(
            backend.convert_to_numpy(x), backend.convert_to_numpy(y)
        )

        self.assertAllClose(op_function(x, y), expected_result)
        self.assertSparseness(op_function(x, y), op_sparseness(x, y))
        self.assertAllClose(op_class()(x, y), expected_result)
        self.assertSparseness(op_class()(x, y), op_sparseness(x, y))

    @parameterized.named_parameters(
        named_product(
            BINARY_OPS_TESTS,
            get_sparseness_combinations(create_indexed_slices),
            dtype=DTYPES,
        )
    )
    def test_binary_correctness_indexed_slices(
        self, x, y, op_function, op_class, np_op, op_sparseness, dtype
    ):
        if dtype == "int32" and op_function.__name__ in ("floor_divide", "mod"):
            self.skipTest(f"{op_function.__name__} does not support integers")

        x = backend.cast(x, dtype)
        y = backend.cast(y, dtype)
        expected_result = np_op(
            backend.convert_to_numpy(x), backend.convert_to_numpy(y)
        )

        self.assertAllClose(op_function(x, y), expected_result)
        self.assertSparseness(op_function(x, y), op_sparseness(x, y))
        self.assertAllClose(op_class()(x, y), expected_result)
        self.assertSparseness(op_class()(x, y), op_sparseness(x, y))

    def test_divide_with_zeros_in_int_sparse_tensor(self):
        x = backend.convert_to_tensor([[0, 2, 3], [3, 2, 1]], dtype="int32")
        x = create_sparse_tensor(x, start=0, delta=2)
        y = backend.convert_to_tensor([[0, 0, 0], [0, 0, 0]], dtype="int32")
        expected_result = np.divide(
            backend.convert_to_numpy(x), backend.convert_to_numpy(y)
        )

        self.assertAllClose(knp.divide(x, y), expected_result)
        self.assertAllClose(knp.Divide()(x, y), expected_result)

    def test_divide_with_zeros_nans_in_float_sparse_tensor(self):
        x = backend.convert_to_tensor([[0, 2, 3], [3, 2, 1]], dtype="float32")
        x = create_sparse_tensor(x, start=0, delta=2)
        y = backend.convert_to_tensor(
            [[np.nan, np.nan, 3], [0, 0, 1]], dtype="float32"
        )
        expected_result = np.divide(
            backend.convert_to_numpy(x), backend.convert_to_numpy(y)
        )

        self.assertAllClose(knp.divide(x, y), expected_result)
        self.assertAllClose(knp.Divide()(x, y), expected_result)

    def test_divide_with_zeros_in_int_indexed_slices(self):
        x = backend.convert_to_tensor([[0, 2, 3], [3, 2, 1]], dtype="int32")
        x = create_indexed_slices(x, start=0, delta=2)
        y = backend.convert_to_tensor([[0, 0, 3], [0, 0, 1]], dtype="int32")
        expected_result = np.divide(
            backend.convert_to_numpy(x), backend.convert_to_numpy(y)
        )

        self.assertAllClose(knp.divide(x, y), expected_result)
        self.assertAllClose(knp.Divide()(x, y), expected_result)

    def test_divide_with_zeros_nans_in_float_indexed_slices(self):
        x = backend.convert_to_tensor([[0, 2, 3], [3, 2, 1]], dtype="float32")
        x = create_indexed_slices(x, start=0, delta=2)
        y = backend.convert_to_tensor(
            [[np.nan, 0, 3], [np.nan, 0, 1]], dtype="float32"
        )
        expected_result = np.divide(
            backend.convert_to_numpy(x), backend.convert_to_numpy(y)
        )

        self.assertAllClose(knp.divide(x, y), expected_result)
        self.assertAllClose(knp.Divide()(x, y), expected_result)


class NumpyDtypeTest(testing.TestCase, parameterized.TestCase):
    """Test the dtype to verify that the behavior matches JAX."""

    # TODO: Using uint64 will lead to weak type promotion (`float`),
    # resulting in different behavior between JAX and Keras. Currently, we
    # are skipping the test for uint64
    ALL_DTYPES = [
        x for x in ALLOWED_DTYPES if x not in ["string", "uint64"]
    ] + [None]
    INT_DTYPES = [x for x in ALLOWED_DTYPES if "int" in x and x != "uint64"]
    FLOAT_DTYPES = [x for x in ALLOWED_DTYPES if "float" in x]

    if backend.backend() == "torch":
        # TODO: torch doesn't support uint16, uint32 and uint64
        ALL_DTYPES = [
            x for x in ALL_DTYPES if x not in ["uint16", "uint32", "uint64"]
        ]
        INT_DTYPES = [
            x for x in INT_DTYPES if x not in ["uint16", "uint32", "uint64"]
        ]

    def setUp(self):
        from jax.experimental import enable_x64

        self.jax_enable_x64 = enable_x64()
        self.jax_enable_x64.__enter__()
        return super().setUp()

    def tearDown(self) -> None:
        self.jax_enable_x64.__exit__(None, None, None)
        return super().tearDown()

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_add(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.add(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.add(x1, x2).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Add().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_add_python_types(self, dtype):
        import jax.experimental
        import jax.numpy as jnp

        # We have to disable x64 for jax since jnp.add doesn't respect
        # JAX_DEFAULT_DTYPE_BITS=32 in `./conftest.py`. We also need to downcast
        # the expected dtype from 64 bit to 32 bit when using jax backend.
        with jax.experimental.disable_x64():
            x = knp.ones((1,), dtype=dtype)
            x_jax = jnp.ones((1,), dtype=dtype)

            # python int
            expected_dtype = standardize_dtype(jnp.add(x_jax, 1).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            elif dtype == "int64":
                expected_dtype = "int64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.add(x, 1).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Add().symbolic_call(x, 1).dtype, expected_dtype
            )

            # python float
            expected_dtype = standardize_dtype(jnp.add(x_jax, 1.0).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.add(x, 1.0).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Add().symbolic_call(x, 1.0).dtype, expected_dtype
            )

    @parameterized.named_parameters(named_product(dtype=INT_DTYPES))
    def test_bincount(self, dtype):
        import jax.numpy as jnp

        if backend.backend() == "tensorflow":
            import tensorflow as tf

            if tf.test.is_gpu_available():
                self.skipTest("bincount does not work in tensorflow gpu")

        x = np.array([1, 1, 2, 3, 2, 4, 4, 5], dtype=dtype)
        weights = np.array([0, 0, 3, 2, 1, 1, 4, 2], dtype=dtype)
        minlength = 3
        self.assertEqual(
            standardize_dtype(
                knp.bincount(x, weights=weights, minlength=minlength).dtype
            ),
            standardize_dtype(
                jnp.bincount(x, weights=weights, minlength=minlength).dtype
            ),
        )
        self.assertEqual(
            knp.Bincount(weights=weights, minlength=minlength)
            .symbolic_call(x)
            .dtype,
            standardize_dtype(
                jnp.bincount(x, weights=weights, minlength=minlength).dtype
            ),
        )

        # test float32 weights
        weights = np.array([0, 0, 3, 2, 1, 1, 4, 2], dtype="float32")
        self.assertEqual(
            standardize_dtype(knp.bincount(x, weights=weights).dtype),
            standardize_dtype(jnp.bincount(x, weights=weights).dtype),
        )
        self.assertEqual(
            knp.Bincount(weights=weights).symbolic_call(x).dtype,
            standardize_dtype(jnp.bincount(x, weights=weights).dtype),
        )

        # test float16 weights
        weights = np.array([0, 0, 3, 2, 1, 1, 4, 2], dtype="float16")
        self.assertEqual(
            standardize_dtype(knp.bincount(x, weights=weights).dtype),
            standardize_dtype(jnp.bincount(x, weights=weights).dtype),
        )
        self.assertEqual(
            knp.Bincount(weights=weights).symbolic_call(x).dtype,
            standardize_dtype(jnp.bincount(x, weights=weights).dtype),
        )

        # test weights=None
        self.assertEqual(
            standardize_dtype(knp.bincount(x).dtype),
            standardize_dtype(jnp.bincount(x).dtype),
        )
        self.assertEqual(
            knp.Bincount().symbolic_call(x).dtype,
            standardize_dtype(jnp.bincount(x).dtype),
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_subtract(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        if dtype1 == "bool" and dtype2 == "bool":
            self.skipTest("subtract does not support bool")

        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.subtract(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.subtract(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Subtract().symbolic_call(x1, x2).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_subtract_python_types(self, dtype):
        import jax.experimental
        import jax.numpy as jnp

        # We have to disable x64 for jax since jnp.subtract doesn't respect
        # JAX_DEFAULT_DTYPE_BITS=32 in `./conftest.py`. We also need to downcast
        # the expected dtype from 64 bit to 32 bit when using jax backend.
        with jax.experimental.disable_x64():
            x = knp.ones((1,), dtype=dtype)
            x_jax = jnp.ones((1,), dtype=dtype)

            # python int
            expected_dtype = standardize_dtype(jnp.subtract(x_jax, 1).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            elif dtype == "int64":
                expected_dtype = "int64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.subtract(x, 1).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Subtract().symbolic_call(x, 1).dtype, expected_dtype
            )

            # python float
            expected_dtype = standardize_dtype(jnp.subtract(x_jax, 1.0).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.subtract(x, 1.0).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Subtract().symbolic_call(x, 1.0).dtype, expected_dtype
            )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_matmul(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.matmul(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.matmul(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Matmul().symbolic_call(x1, x2).dtype, expected_dtype
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_multiply(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.multiply(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.multiply(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Multiply().symbolic_call(x1, x2).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_multiply_python_types(self, dtype):
        import jax.experimental
        import jax.numpy as jnp

        # We have to disable x64 for jax since jnp.multiply doesn't respect
        # JAX_DEFAULT_DTYPE_BITS=32 in `./conftest.py`. We also need to downcast
        # the expected dtype from 64 bit to 32 bit when using jax backend.
        with jax.experimental.disable_x64():
            x = knp.ones((1,), dtype=dtype)
            x_jax = jnp.ones((1,), dtype=dtype)

            # python int
            expected_dtype = standardize_dtype(jnp.multiply(x_jax, 1).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            elif dtype == "int64":
                expected_dtype = "int64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.multiply(x, 1).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Multiply().symbolic_call(x, 1).dtype, expected_dtype
            )

            # python float
            expected_dtype = standardize_dtype(jnp.multiply(x_jax, 1.0).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.multiply(x, 1.0).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Multiply().symbolic_call(x, 1.0).dtype, expected_dtype
            )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_mean(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.mean(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = "float32"

        self.assertEqual(standardize_dtype(knp.mean(x).dtype), expected_dtype)
        self.assertEqual(knp.Mean().symbolic_call(x).dtype, expected_dtype)

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_max(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.max(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.max(x).dtype), expected_dtype)
        self.assertEqual(knp.Max().symbolic_call(x).dtype, expected_dtype)

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_ones(self, dtype):
        import jax.numpy as jnp

        expected_dtype = standardize_dtype(jnp.ones([2, 3], dtype=dtype).dtype)

        self.assertEqual(
            standardize_dtype(knp.ones([2, 3], dtype=dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Ones().symbolic_call([2, 3], dtype=dtype).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_zeros(self, dtype):
        import jax.numpy as jnp

        expected_dtype = standardize_dtype(jnp.zeros([2, 3], dtype=dtype).dtype)

        self.assertEqual(
            standardize_dtype(knp.zeros([2, 3], dtype=dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Zeros().symbolic_call([2, 3], dtype=dtype).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_absolute(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.absolute(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.absolute(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Absolute().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_all(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.all(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.all(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.All().symbolic_call(x).dtype), expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_amax(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.amax(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.amax(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Amax().symbolic_call(x).dtype), expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_amin(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.amin(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.amin(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Amin().symbolic_call(x).dtype), expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_any(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.any(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.any(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Any().symbolic_call(x).dtype), expected_dtype
        )

    # TODO: test_einsum

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_append(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.append(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.append(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Append().symbolic_call(x1, x2).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_argmax(self, dtype):
        import jax.numpy as jnp

        if dtype == "bool":
            value = [[True, False, True], [False, True, False]]
        else:
            value = [[1, 2, 3], [3, 2, 1]]
        x = knp.array(value, dtype=dtype)
        x_jax = jnp.array(value, dtype=dtype)
        expected_dtype = standardize_dtype(jnp.argmax(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.argmax(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Argmax().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_argmin(self, dtype):
        import jax.numpy as jnp

        if dtype == "bool":
            value = [[True, False, True], [False, True, False]]
        else:
            value = [[1, 2, 3], [3, 2, 1]]
        x = knp.array(value, dtype=dtype)
        x_jax = jnp.array(value, dtype=dtype)
        expected_dtype = standardize_dtype(jnp.argmin(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.argmin(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Argmin().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_argsort(self, dtype):
        import jax.numpy as jnp

        if dtype == "bool":
            value = [[True, False, True], [False, True, False]]
        else:
            value = [[1, 2, 3], [4, 5, 6]]
        x = knp.array(value, dtype=dtype)
        x_jax = jnp.array(value, dtype=dtype)
        expected_dtype = standardize_dtype(jnp.argsort(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.argsort(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Argsort().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.parameters(
        (10, None, 1, None),
        (0, 10, 1, None),
        (0, 10, 0.5, None),
        (10.0, None, 1, None),
        (0, 10.0, 1, None),
        (0.0, 10, 1, None),
        (10, None, 1, "float32"),
        (10, None, 1, "int32"),
    )
    def test_arange(self, start, stop, step, dtype):
        import jax.numpy as jnp

        expected_dtype = standardize_dtype(
            jnp.arange(start, stop, step, dtype).dtype
        )

        self.assertEqual(
            standardize_dtype(knp.arange(start, stop, step, dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Arange().symbolic_call(start, stop, step, dtype).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_arccos(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.arccos(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.arccos(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Arccos().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_arccosh(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.arccosh(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.arccosh(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Arccosh().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_arcsin(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.arcsin(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.arcsin(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Arcsin().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_arcsinh(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.arcsinh(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.arcsinh(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Arcsinh().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_arctan(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.arctan(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.arctan(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Arctan().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_arctan2(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.arctan2(x1_jax, x2_jax).dtype)
        if dtype1 is not None and "float" not in dtype1:
            if dtype2 is not None and "float" not in dtype2:
                if "int64" in (dtype1, dtype2) or "uint32" in (dtype1, dtype2):
                    expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.arctan2(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Arctan2().symbolic_call(x1, x2).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_arctanh(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.arctanh(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.arctanh(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Arctanh().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.parameters(
        (bool(0), "bool"),
        (int(0), "int32"),
        (float(0), backend.floatx()),
        ([False, True, False], "bool"),
        ([1, 2, 3], "int32"),
        ([1.0, 2.0, 3.0], backend.floatx()),
        ([1, 2.0, 3], backend.floatx()),
        ([[False], [True], [False]], "bool"),
        ([[1], [2], [3]], "int32"),
        ([[1], [2.0], [3]], backend.floatx()),
        *[
            (np.array(0, dtype=dtype), dtype)
            for dtype in ALL_DTYPES
            if dtype is not None
        ],
    )
    def test_array(self, x, expected_dtype):
        # We have to disable x64 for jax backend since jnp.array doesn't respect
        # JAX_DEFAULT_DTYPE_BITS=32 in `./conftest.py`. We also need to downcast
        # the expected dtype from 64 bit to 32 bit.
        if backend.backend() == "jax":
            import jax.experimental

            jax_disable_x64 = jax.experimental.disable_x64()
            expected_dtype = expected_dtype.replace("64", "32")
        else:
            jax_disable_x64 = contextlib.nullcontext()

        with jax_disable_x64:
            self.assertEqual(
                standardize_dtype(knp.array(x).dtype), expected_dtype
            )
        # TODO: support the assertion of knp.Array

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_average(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(
            jnp.average(x1_jax, weights=x2_jax).dtype
        )
        if dtype1 is not None and "float" not in dtype1:
            if dtype2 is not None and "float" not in dtype2:
                if "int64" in (dtype1, dtype2) or "uint32" in (dtype1, dtype2):
                    expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.average(x1, weights=x2).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Average().symbolic_call(x1, weights=x2).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_broadcast_to(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((3,), dtype=dtype)
        x_jax = jnp.ones((3,), dtype=dtype)
        expected_dtype = standardize_dtype(
            jnp.broadcast_to(x_jax, (3, 3)).dtype
        )

        self.assertEqual(
            standardize_dtype(knp.broadcast_to(x, (3, 3)).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.BroadcastTo((3, 3)).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_ceil(self, dtype):
        import jax.numpy as jnp

        if dtype is None:
            dtype = backend.floatx()
        if dtype == "bool":
            value = [[True, False, True], [True, False, True]]
        elif "int" in dtype:
            value = [[1, 2, 2], [2, 11, 5]]
        else:
            value = [[1.2, 2.1, 2.5], [2.4, 11.9, 5.5]]
        x = knp.array(value, dtype=dtype)
        x_jax = jnp.array(value, dtype=dtype)
        expected_dtype = standardize_dtype(jnp.ceil(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.ceil(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Ceil().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_clip(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.clip(x_jax, -2, 2).dtype)

        self.assertEqual(
            standardize_dtype(knp.clip(x, -2, 2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Clip(-2, 2).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_concatenate(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(
            jnp.concatenate([x1_jax, x2_jax]).dtype
        )

        self.assertEqual(
            standardize_dtype(knp.concatenate([x1, x2]).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Concatenate().symbolic_call([x1, x2]).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_cos(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.cos(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.cos(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Cos().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_cosh(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.cosh(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.cosh(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Cosh().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_copy(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.copy(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.copy(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Copy().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_count_nonzero(self, dtype):
        x = knp.ones((1,), dtype=dtype)
        expected_dtype = "int32"

        self.assertEqual(
            standardize_dtype(knp.count_nonzero(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.CountNonzero().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_cross(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1, 1, 3), dtype=dtype1)
        x2 = knp.ones((1, 1, 3), dtype=dtype2)
        x1_jax = jnp.ones((1, 1, 3), dtype=dtype1)
        x2_jax = jnp.ones((1, 1, 3), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.cross(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.cross(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Cross().symbolic_call(x1, x2).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_diag(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.diag(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.diag(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Diag().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_diagonal(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1, 1, 1), dtype=dtype)
        x_jax = jnp.ones((1, 1, 1), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.diagonal(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.diagonal(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Diagonal().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_diff(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.diff(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.diff(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Diff().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_digitize(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        bins = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        x_bins = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.digitize(x_jax, x_bins).dtype)

        self.assertEqual(
            standardize_dtype(knp.digitize(x, bins).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Digitize().symbolic_call(x, bins).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_divide(self, dtypes):
        import jax.experimental
        import jax.numpy as jnp

        # We have to disable x64 for jax since jnp.divide doesn't respect
        # JAX_DEFAULT_DTYPE_BITS=32 in `./conftest.py`. We also need to downcast
        # the expected dtype from 64 bit to 32 bit when using jax backend.
        with jax.experimental.disable_x64():
            dtype1, dtype2 = dtypes
            x1 = knp.ones((1,), dtype=dtype1)
            x2 = knp.ones((1,), dtype=dtype2)
            x1_jax = jnp.ones((1,), dtype=dtype1)
            x2_jax = jnp.ones((1,), dtype=dtype2)
            expected_dtype = standardize_dtype(jnp.divide(x1_jax, x2_jax).dtype)
            if "float64" in (dtype1, dtype2):
                expected_dtype = "float64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.divide(x1, x2).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Divide().symbolic_call(x1, x2).dtype, expected_dtype
            )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_divide_python_types(self, dtype):
        import jax.experimental
        import jax.numpy as jnp

        # We have to disable x64 for jax since jnp.divide doesn't respect
        # JAX_DEFAULT_DTYPE_BITS=32 in `./conftest.py`. We also need to downcast
        # the expected dtype from 64 bit to 32 bit when using jax backend.
        with jax.experimental.disable_x64():
            x = knp.ones((), dtype=dtype)
            x_jax = jnp.ones((), dtype=dtype)

            # python int
            expected_dtype = standardize_dtype(jnp.divide(x_jax, 1).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.divide(x, 1).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Divide().symbolic_call(x, 1).dtype, expected_dtype
            )

            # python float
            expected_dtype = standardize_dtype(jnp.divide(x_jax, 1.0).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.divide(x, 1.0).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Divide().symbolic_call(x, 1.0).dtype, expected_dtype
            )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_dot(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((2, 3, 4), dtype=dtype1)
        x2 = knp.ones((4, 3), dtype=dtype2)
        x1_jax = jnp.ones((2, 3, 4), dtype=dtype1)
        x2_jax = jnp.ones((4, 3), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.dot(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.dot(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(knp.Dot().symbolic_call(x1, x2).dtype, expected_dtype)

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_einsum(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1, 1, 1), dtype=dtype1)
        x2 = knp.ones((1, 1, 1), dtype=dtype2)
        x1_jax = jnp.ones((1, 1, 1), dtype=dtype1)
        x2_jax = jnp.ones((1, 1, 1), dtype=dtype2)
        subscripts = "ijk,lkj->il"
        expected_dtype = standardize_dtype(
            jnp.einsum(subscripts, x1_jax, x2_jax).dtype
        )

        self.assertEqual(
            standardize_dtype(knp.einsum(subscripts, x1, x2).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Einsum(subscripts).symbolic_call(x1, x2).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_empty(self, dtype):
        import jax.numpy as jnp

        expected_dtype = standardize_dtype(jnp.empty([2, 3], dtype=dtype).dtype)

        self.assertEqual(
            standardize_dtype(knp.empty([2, 3], dtype=dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Empty().symbolic_call([2, 3], dtype=dtype).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_equal(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.equal(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.equal(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Equal().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_exp(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.exp(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.exp(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Exp().symbolic_call(x).dtype), expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_expand_dims(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.expand_dims(x_jax, -1).dtype)

        self.assertEqual(
            standardize_dtype(knp.expand_dims(x, -1).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.ExpandDims(-1).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_expm1(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.expm1(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.expm1(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Expm1().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_eye(self, dtype):
        import jax.numpy as jnp

        expected_dtype = standardize_dtype(jnp.eye(3, dtype=dtype).dtype)

        self.assertEqual(
            standardize_dtype(knp.eye(3, dtype=dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Eye().symbolic_call(3, dtype=dtype).dtype),
            expected_dtype,
        )

        expected_dtype = standardize_dtype(jnp.eye(3, 4, 1, dtype=dtype).dtype)

        self.assertEqual(
            standardize_dtype(knp.eye(3, 4, 1, dtype=dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Eye().symbolic_call(3, 4, 1, dtype=dtype).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_flip(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.flip(x_jax, -1).dtype)

        self.assertEqual(
            standardize_dtype(knp.flip(x, -1).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Flip(-1).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_floor(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.floor(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.floor(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Floor().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_full(self, dtype):
        import jax.numpy as jnp

        expected_dtype = standardize_dtype(jnp.full((), 0, dtype=dtype).dtype)
        if dtype is None:
            expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.full((), 0, dtype=dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Full().symbolic_call((), 0, dtype=dtype).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_full_like(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.full_like(x_jax, 0).dtype)

        self.assertEqual(
            standardize_dtype(knp.full_like(x, 0).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.FullLike().symbolic_call(x, 0).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_greater(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.greater(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.greater(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Greater().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_greater_equal(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(
            jnp.greater_equal(x1_jax, x2_jax).dtype
        )

        self.assertEqual(
            standardize_dtype(knp.greater_equal(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.GreaterEqual().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_hstack(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1, 1), dtype=dtype1)
        x2 = knp.ones((1, 1), dtype=dtype2)
        x1_jax = jnp.ones((1, 1), dtype=dtype1)
        x2_jax = jnp.ones((1, 1), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.hstack([x1_jax, x2_jax]).dtype)

        self.assertEqual(
            standardize_dtype(knp.hstack([x1, x2]).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Hstack().symbolic_call([x1, x2]).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_identity(self, dtype):
        import jax.numpy as jnp

        expected_dtype = standardize_dtype(jnp.identity(3, dtype=dtype).dtype)

        self.assertEqual(
            standardize_dtype(knp.identity(3, dtype=dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Identity().symbolic_call(3, dtype=dtype).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_isclose(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.isclose(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.isclose(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Isclose().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_isfinite(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.isfinite(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.isfinite(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Isfinite().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_isinf(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.isinf(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.isinf(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Isinf().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_isnan(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.isnan(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.isnan(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Isnan().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_less(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.less(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.less(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Less().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_less_equal(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.less_equal(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.less_equal(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.LessEqual().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(
            start_and_stop=[
                [0, 10],
                [0.5, 10.5],
                [np.array([0, 1], "int32"), np.array([10, 20], "int32")],
                [np.array([0, 1], "float32"), np.array([10, 20], "float32")],
            ],
            num=[0, 1, 5],
            dtype=FLOAT_DTYPES + [None],
        )
    )
    def test_linspace(self, start_and_stop, num, dtype):
        import jax.numpy as jnp

        start, stop = start_and_stop
        expected_dtype = standardize_dtype(
            jnp.linspace(start, stop, num, dtype=dtype).dtype
        )

        self.assertEqual(
            standardize_dtype(
                knp.linspace(start, stop, num, dtype=dtype).dtype
            ),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Linspace(num, dtype=dtype).symbolic_call(start, stop).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_log(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((3, 3), dtype=dtype)
        x_jax = jnp.ones((3, 3), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.log(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.log(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Log().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_log10(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((3, 3), dtype=dtype)
        x_jax = jnp.ones((3, 3), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.log10(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.log10(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Log10().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_log1p(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((3, 3), dtype=dtype)
        x_jax = jnp.ones((3, 3), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.log1p(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.log1p(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Log1p().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_log2(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((3, 3), dtype=dtype)
        x_jax = jnp.ones((3, 3), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.log2(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.log2(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Log2().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_logaddexp(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((3, 3), dtype=dtype1)
        x2 = knp.ones((3, 3), dtype=dtype2)
        x1_jax = jnp.ones((3, 3), dtype=dtype1)
        x2_jax = jnp.ones((3, 3), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.logaddexp(x1_jax, x2_jax).dtype)
        # jnp.logaddexp will promote "int64" and "uint32" to "float64"
        # force the promotion to `backend.floatx()`
        if dtype1 is not None and "float" not in dtype1:
            if dtype2 is not None and "float" not in dtype2:
                if "int64" in (dtype1, dtype2) or "uint32" in (dtype1, dtype2):
                    expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.logaddexp(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Logaddexp().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(
            start_and_stop=[
                [0, 10],
                [0.5, 10.5],
                [np.array([0, 1], "int32"), np.array([10, 20], "int32")],
                [np.array([0, 1], "float32"), np.array([10, 20], "float32")],
            ],
            num=[0, 1, 5],
            dtype=FLOAT_DTYPES + [None],
        )
    )
    def test_logspace(self, start_and_stop, num, dtype):
        import jax.numpy as jnp

        start, stop = start_and_stop
        expected_dtype = standardize_dtype(
            jnp.logspace(start, stop, num, dtype=dtype).dtype
        )

        self.assertEqual(
            standardize_dtype(
                knp.logspace(start, stop, num, dtype=dtype).dtype
            ),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(
                knp.Logspace(num, dtype=dtype).symbolic_call(start, stop).dtype
            ),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_logical_and(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(
            jnp.logical_and(x1_jax, x2_jax).dtype
        )

        self.assertEqual(
            standardize_dtype(knp.logical_and(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.LogicalAnd().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_logical_not(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.logical_not(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.logical_not(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.LogicalNot().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_logical_or(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.logical_or(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.logical_or(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.LogicalOr().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_logical_xor(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(
            jnp.logical_xor(x1_jax, x2_jax).dtype
        )

        self.assertEqual(
            standardize_dtype(knp.logical_xor(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.LogicalXor().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_maximum(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.maximum(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.maximum(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Maximum().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_maximum_python_types(self, dtype):
        import jax.experimental
        import jax.numpy as jnp

        # We have to disable x64 for jax since jnp.maximum doesn't respect
        # JAX_DEFAULT_DTYPE_BITS=32 in `./conftest.py`.
        with jax.experimental.disable_x64():
            x = knp.ones((), dtype=dtype)
            x_jax = jnp.ones((), dtype=dtype)

            # python int
            expected_dtype = standardize_dtype(jnp.maximum(x_jax, 1).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            elif dtype == "int64":
                expected_dtype = "int64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.maximum(x, 1).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Maximum().symbolic_call(x, 1).dtype, expected_dtype
            )

            # python float
            expected_dtype = standardize_dtype(jnp.maximum(x_jax, 1.0).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.maximum(x, 1.0).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Maximum().symbolic_call(x, 1.0).dtype, expected_dtype
            )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_median(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((3, 3), dtype=dtype)
        x_jax = jnp.ones((3, 3), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.median(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.median(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Median().symbolic_call(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.median(x, axis=1).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Median(axis=1).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_meshgrid(self, dtype):
        import jax.numpy as jnp

        if dtype == "bool":
            self.skipTest("meshgrid doesn't support bool dtype")
        elif dtype is None:
            dtype = backend.floatx()
        x = knp.array([1, 2, 3], dtype=dtype)
        y = knp.array([4, 5, 6], dtype=dtype)
        x_jax = jnp.array([1, 2, 3], dtype=dtype)
        y_jax = jnp.array([4, 5, 6], dtype=dtype)
        expected_dtype = standardize_dtype(jnp.meshgrid(x_jax, y_jax)[0].dtype)

        self.assertEqual(
            standardize_dtype(knp.meshgrid(x, y)[0].dtype), expected_dtype
        )
        self.assertEqual(
            knp.Meshgrid().symbolic_call(x, y)[0].dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_min(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.min(x_jax).dtype)

        self.assertEqual(standardize_dtype(knp.min(x).dtype), expected_dtype)
        self.assertEqual(knp.Min().symbolic_call(x).dtype, expected_dtype)

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_minimum(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.minimum(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.minimum(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Minimum().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_minimum_python_types(self, dtype):
        import jax.experimental
        import jax.numpy as jnp

        # We have to disable x64 for jax since jnp.minimum doesn't respect
        # JAX_DEFAULT_DTYPE_BITS=32 in `./conftest.py`.
        with jax.experimental.disable_x64():
            x = knp.ones((), dtype=dtype)
            x_jax = jnp.ones((), dtype=dtype)

            # python int
            expected_dtype = standardize_dtype(jnp.minimum(x_jax, 1).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            elif dtype == "int64":
                expected_dtype = "int64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.minimum(x, 1).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Minimum().symbolic_call(x, 1).dtype, expected_dtype
            )

            # python float
            expected_dtype = standardize_dtype(jnp.minimum(x_jax, 1.0).dtype)
            if dtype == "float64":
                expected_dtype = "float64"
            if backend.backend() == "jax":
                expected_dtype = expected_dtype.replace("64", "32")

            self.assertEqual(
                standardize_dtype(knp.minimum(x, 1.0).dtype), expected_dtype
            )
            self.assertEqual(
                knp.Minimum().symbolic_call(x, 1.0).dtype, expected_dtype
            )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_mod(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.mod(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.mod(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Mod().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_moveaxis(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1, 1, 1), dtype=dtype)
        x_jax = jnp.ones((1, 1, 1), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.moveaxis(x_jax, -2, -1).dtype)

        self.assertEqual(
            standardize_dtype(knp.moveaxis(x, -2, -1).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Moveaxis(-2, -1).symbolic_call(x).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_nan_to_num(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.nan_to_num(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.nan_to_num(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.NanToNum().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_not_equal(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((), dtype=dtype1)
        x2 = knp.ones((), dtype=dtype2)
        x1_jax = jnp.ones((), dtype=dtype1)
        x2_jax = jnp.ones((), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.not_equal(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.not_equal(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.NotEqual().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_ones_like(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.ones_like(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.ones_like(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.OnesLike().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_outer(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1, 2), dtype=dtype1)
        x2 = knp.ones((3, 4), dtype=dtype2)
        x1_jax = jnp.ones((1, 2), dtype=dtype1)
        x2_jax = jnp.ones((3, 4), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.outer(x1_jax, x2_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.outer(x1, x2).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.Outer().symbolic_call(x1, x2).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_pad(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((2, 2, 2, 2), dtype=dtype)
        x_jax = jnp.ones((2, 2, 2, 2), dtype=dtype)
        pad_width = ((0, 0), (1, 1), (1, 1), (1, 1))

        for mode in ("constant", "symmetric", "reflect"):
            expected_dtype = standardize_dtype(
                jnp.pad(x_jax, pad_width, mode).dtype
            )

            self.assertEqual(
                standardize_dtype(knp.pad(x, pad_width, mode).dtype),
                expected_dtype,
            )
            self.assertEqual(
                standardize_dtype(
                    knp.Pad(pad_width, mode).symbolic_call(x).dtype
                ),
                expected_dtype,
            )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_prod(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1, 1, 1), dtype=dtype)
        x_jax = jnp.ones((1, 1, 1), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.prod(x_jax).dtype)
        # TODO: torch doesn't support uint32
        if backend.backend() == "torch" and expected_dtype == "uint32":
            expected_dtype = "int32"

        self.assertEqual(
            standardize_dtype(knp.prod(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Prod().symbolic_call(x).dtype), expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_quantile(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((3,), dtype=dtype)
        x_jax = jnp.ones((3,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.quantile(x_jax, 0.5).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.quantile(x, 0.5).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Quantile().symbolic_call(x, 0.5).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_ravel(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.ravel(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.ravel(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Ravel().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_repeat(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1, 1), dtype=dtype)
        x_jax = jnp.ones((1, 1), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.repeat(x_jax, 2).dtype)

        self.assertEqual(
            standardize_dtype(knp.repeat(x, 2).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Repeat(2).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_reshape(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1, 1), dtype=dtype)
        x_jax = jnp.ones((1, 1), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.reshape(x_jax, [1]).dtype)

        self.assertEqual(
            standardize_dtype(knp.reshape(x, [1]).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Reshape([1]).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_roll(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((5,), dtype=dtype)
        x_jax = jnp.ones((5,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.roll(x_jax, 2).dtype)

        self.assertEqual(
            standardize_dtype(knp.roll(x, 2).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Roll(2).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_round(self, dtype):
        import jax.numpy as jnp

        if dtype == "bool":
            self.skipTest("round doesn't support bool dtype")
        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.round(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.round(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Round().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_sign(self, dtype):
        import jax.numpy as jnp

        if dtype == "bool":
            self.skipTest("sign doesn't support bool dtype")
        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.sign(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.sign(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Sign().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_sin(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.sin(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.sin(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Sin().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_sinh(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.sinh(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.sinh(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Sinh().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_sort(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((2,), dtype=dtype)
        x_jax = jnp.ones((2,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.sort(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.sort(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Sort().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_split(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1, 2), dtype=dtype)
        x_jax = jnp.ones((1, 2), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.split(x_jax, 2, -1)[0].dtype)

        self.assertEqual(
            standardize_dtype(knp.split(x, 2, -1)[0].dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Split(2, -1).symbolic_call(x)[0].dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_sqrt(self, dtype):
        import jax.numpy as jnp

        x1 = knp.ones((1,), dtype=dtype)
        x1_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.sqrt(x1_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.sqrt(x1).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Sqrt().symbolic_call(x1).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_square(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.square(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.square(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Square().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_squeeze(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1, 1), dtype=dtype)
        x_jax = jnp.ones((1, 1), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.squeeze(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.squeeze(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Squeeze().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(
        named_product(dtypes=itertools.combinations(ALL_DTYPES, 2))
    )
    def test_stack(self, dtypes):
        import jax.numpy as jnp

        dtype1, dtype2 = dtypes
        x1 = knp.ones((1,), dtype=dtype1)
        x2 = knp.ones((1,), dtype=dtype2)
        x1_jax = jnp.ones((1,), dtype=dtype1)
        x2_jax = jnp.ones((1,), dtype=dtype2)
        expected_dtype = standardize_dtype(jnp.stack([x1_jax, x2_jax]).dtype)

        self.assertEqual(
            standardize_dtype(knp.stack([x1, x2]).dtype), expected_dtype
        )
        self.assertEqual(
            knp.Stack().symbolic_call([x1, x2]).dtype, expected_dtype
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_std(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.std(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(
            standardize_dtype(knp.std(x).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Std().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_sum(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.sum(x_jax).dtype)

        # TODO: torch doesn't support uint32
        if backend.backend() == "torch" and expected_dtype == "uint32":
            expected_dtype = "int32"

        self.assertEqual(standardize_dtype(knp.sum(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Sum().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_swapaxes(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1, 1), dtype=dtype)
        x_jax = jnp.ones((1, 1), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.swapaxes(x_jax, -1, -2).dtype)

        self.assertEqual(
            standardize_dtype(knp.swapaxes(x, -1, -2).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Swapaxes(-1, -2).symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_tan(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.tan(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.tan(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Tan().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_tanh(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((1,), dtype=dtype)
        x_jax = jnp.ones((1,), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.tanh(x_jax).dtype)
        if dtype == "int64":
            expected_dtype = backend.floatx()

        self.assertEqual(standardize_dtype(knp.tanh(x).dtype), expected_dtype)
        self.assertEqual(
            standardize_dtype(knp.Tanh().symbolic_call(x).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_tri(self, dtype):
        import jax.numpy as jnp

        expected_dtype = standardize_dtype(jnp.tri(3, dtype=dtype).dtype)

        self.assertEqual(
            standardize_dtype(knp.tri(3, dtype=dtype).dtype),
            expected_dtype,
        )
        self.assertEqual(
            standardize_dtype(knp.Tri().symbolic_call(3, dtype=dtype).dtype),
            expected_dtype,
        )

    @parameterized.named_parameters(named_product(dtype=ALL_DTYPES))
    def test_zeros_like(self, dtype):
        import jax.numpy as jnp

        x = knp.ones((), dtype=dtype)
        x_jax = jnp.ones((), dtype=dtype)
        expected_dtype = standardize_dtype(jnp.ones_like(x_jax).dtype)

        self.assertEqual(
            standardize_dtype(knp.zeros_like(x).dtype), expected_dtype
        )
        self.assertEqual(
            standardize_dtype(knp.ZerosLike().symbolic_call(x).dtype),
            expected_dtype,
        )
