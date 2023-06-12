def find_slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    return (m, b)


print(find_slope([41.62541966,-73.78459166], [41.62555333,-73.784495]))