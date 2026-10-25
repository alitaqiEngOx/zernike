""" Licensed under the same terms as described in the main 
licensing script of this repository. """

    # filter out incorrect entries
    #if (
    #    (j is None and mn is None) or
    #    (j is not None and mn is not None)
    #):
    #    raise ValueError(
    #        "provide either `j` or `mn`"
    #    )

    #if j is None:
    #    j = mn_to_j(mn[0], mn[1])
    #    print(f"j = {j}")
    #    return

    #m, n = j_to_mn(j)
    #print(f"m = {m}; n = {n}")

        #npz = NPZ(npz_path)

        # work on `show_info`

        #npz.dump(
        #    save_as, key=_key, index=index 
        #)

    #npz = NPZ(npz_path)

    #if show_info:
    #    info = [
    #        item.split(':', maxsplit=1)
    #        for item in npz.keys_and_shapes
    #    ]

    #    key_width = max(
    #        len(key) for key, _ in info
    #    )

    #    print(f"{'key':<{key_width}} : shape")

    #    for key, shape in info:
    #        print(f"{key:<{key_width}} : {shape}")

    #    return

    #if save_as is None:
    #    raise ValueError(
    #        "provide either `show_info=True` or `save_as` path"
    #    )

    #npz.dump(
    #    save_as, key=key, index=index
    #)