cc_library(
    name = "Node",
    srcs = ["Node.cpp"],
    hdrs = ["Node.h"],
    visibility = ["//visibility:public"],
)

cc_test(
    name = "NodeTest",
    srcs = [
        "Node.h",
        "Node.cpp",
        "Node.test.cpp",
    ],
    deps = ["@googletest//:gtest_main"],
    data = [],
)