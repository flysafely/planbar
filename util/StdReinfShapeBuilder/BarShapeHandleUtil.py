"""
Implementation of the bar shape handle utilities
"""

import NemAll_Python_Geometry as AllplanGeo

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


def get_handle_from_shape(reinf_def, shape, handle_list, handle_id, build_ele):
    """
    Create the handle from a shape

    Args:
        reinf_def:    reinforcement definition
        shape:        bending shape
        handle_list:  list with the handle
        handle_id:    ID of the handle
    """

    handle = reinf_def.get_attribute("Handle")

    if not handle:
        return

    handle_data_list = handle.split(";");

    for handle_data in handle_data_list:
        handle_param_list = handle_data.split(",")

        shape_pol = shape.GetShapePolyline()

        handle_index = int(handle_param_list[1])
        ref_index    = int(handle_param_list[2])

        if handle_index > shape_pol.Count()  or  ref_index > shape_pol.Count():
            continue

        dir_line = AllplanGeo.Line3D(shape_pol.GetPoint(handle_index - 1), shape_pol.GetPoint(ref_index - 1))

        length = getattr(build_ele, handle_param_list[0], None)

        if not length:
            return

        length = length.value

        if abs(length) < 1:
            continue

        delta = AllplanGeo.CalcLength(dir_line) - length

        dir_line.TrimEnd(delta)

        handle_list.append(HandleProperties(handle_id,
                                            dir_line.StartPoint, dir_line.EndPoint,
                                            [(handle_param_list[0], HandleDirection.point_dir)],
                                            HandleDirection.point_dir))
