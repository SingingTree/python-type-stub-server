from another_package.widget_factory import make_widget_matrix
from test_package.blorgle import calibrate_blorgle
from test_package.nested_package.splines import reticulate


def main():
    widget_matrix = make_widget_matrix(7)
    print(widget_matrix)
    calibrate_blorgle(widget_matrix[2])
    blogsons_number = reticulate(7, 2)
    print(blogsons_number)


if __name__ == "__main__":
    main()
