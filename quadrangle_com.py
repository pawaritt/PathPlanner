BASE_LINE = {
    '3012': 1,
    '0312': 3,
    '3021': 1,
    '0321': 1
}
MAXIMUM_SPLIT_POINT = {
    '3012': 
    [
        {
            'line': 4,
            'point': 2
        }, 
        ],
    '0312': 
    [
        {
            'line': 1,
            'point': 3
        }, {
            'line': 4,
            'point': 2
        }
    ],
    '3021': 
    [
        {
            'line': 4,
            'point': 2
        }, {
            'line': 2,
            'point': 1
        }
    ],
    '0321': 
    [
        {
            'line': 1,
            'point': 3
        }, {
            'line': 4,
            'point': 2
        }, {
            'line': 2,
            'point': 1
            }
    ],
}
MINIMUMLINE_SPLIT_POINT = {
    '3012': 
    [
        {
            'line': 1,
            'point': 0
        }, {
            'line': 3,
            'point': 1
        }, {
            'line': 2,
            'point': 2
            }
        ],
    '0312': 
    [
        {
            'line': 3,
            'point': 1
        }, {
            'line': 2,
            'point': 2
        }
    ],
    '3021': 
    [
        {
            'line': 1,
            'point': 0
        }, {
            'line': 3,
            'point': 1
        }
    ],
    '0321': 
    [
        {
            'line': 3,
            'point': 1
        }, 
    ],
}