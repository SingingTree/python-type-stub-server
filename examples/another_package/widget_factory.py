def make_widget_matrix(num_widgets):
    print(f"making {num_widgets} widgets")
    widget_matrix = []
    for row in range(num_widgets):
        row_list = []
        for col in range(num_widgets):
            num = 0
            if col == row:
                num = 1
            row_list.append(num)
        widget_matrix.append(row_list)
    return widget_matrix
