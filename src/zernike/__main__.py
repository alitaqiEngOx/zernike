import argparse

from operations import pipeline


def main() -> None:
    """
    Pipeline entry point.
    """
    args = parse_args()

    pipeline.run(
        j=args.j, rho=args.max_radius, rho_step=args.radius_step, 
        num_theta=args.num_angle_steps
    )


def parse_args() -> argparse.Namespace:
    """
    Parses command line arguments.

    cmd Arguments
    -------------
    j: int
        order of the Zernike polynomial.
    
    --max_radius (optional): float
        maximum radius to be included in the plot
        (defaults to 1.0).

    --num_angle_steps (optional): int
        number of angles to be computed between 0 deg and 360 deg
        (defaults to 100).

    --radius_step (optional): float
        numerical step in the radius domain
        (defaults to 0.01).

    Returns
    -------
    argparse.Namespace class instance enclosing the parsed
    cmd arguments.
    """
    parser = argparse.ArgumentParser(
        description="Zernike plots",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "j",
        type=int,
        help="order of the Zernike polynomial",
    )
    parser.add_argument(
        "--max_radius",
        type=float,
        default=1.,
        help="maximum radius to be included in the plot",
    )
    parser.add_argument(
        "--num_angle_steps",
        type=int,
        default=100,
        help="number of angles to be computed between 0 deg and 360 deg",
    )
    parser.add_argument(
        "--radius_step",
        type=float,
        default=0.01,
        help="numerical step in the radius domain",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()