import argparse
import logging
import uuid

from model_orchestrator.model_orchestrator import ModelOrchestrator

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    # Run kmv model
    # Example CMD: python3 main.py kmv 1000000 900000 500000 0.18 0.12

    # Run a monte carlo simulation (mcs) with GBM model to predict future asset path
    # Example CMD: python3 main.py mcs gbm 1000 200 0.2 0.18 365 250

    namespace = "rqmp"

    parser = argparse.ArgumentParser("Prototype Risk Quant Model Platform")

    subparsers = parser.add_subparsers(dest="subcommand")

    # KMV Model
    parser_kmv = subparsers.add_parser("kmv")
    parser_kmv.add_argument("enterprise_value", help="Enterprise value", type=float)
    parser_kmv.add_argument("short_term_debt", help="Short term debt", type=float)
    parser_kmv.add_argument("long_term_debt", help="Long term debt", type=float)
    parser_kmv.add_argument("mu", help="Expected annual growth rate", type=float)
    parser_kmv.add_argument("sigma", help="Expected annual volatility", type=float)

    # Geometric Brownian Motion Model
    parser_gbm = subparsers.add_parser("mcs")
    parser_gbm.add_argument("model_name", help="model", type=str)
    parser_gbm.add_argument("num_simulations", help="Number of simulations", type=int)
    parser_gbm.add_argument("starting_value", help="Starting value", type=float)
    parser_gbm.add_argument("mu", help="Expected annual return", type=float)
    parser_gbm.add_argument("sigma", help="Expected annual volatility", type=float)
    parser_gbm.add_argument("forecast_period", help="Forecast period in days", type=int)
    parser_gbm.add_argument(
        "num_trading_days", help="Number of trading days in year", type=int
    )

    args = parser.parse_args()

    if args.subcommand == "kmv":

        logging.info("Executing KMV model task.")

        container_params = dict(
            name="credit-models",
            image_pull_policy="Never",
            image="credit-models:latest",
            args=[
                args.enterprise_value,
                args.short_term_debt,
                args.long_term_debt,
                args.mu,
                args.sigma,
            ],
        )

        pod_params = dict(
            name=f"cm-{uuid.uuid4()}",
            restart_policy="Never",
            labels=dict(name="credit-models", type="pod"),
        )

        job_params = dict(
            name=f"cm-{uuid.uuid4()}", labels=dict(name="credit-models", type="job")
        )

        kube_object = ModelOrchestrator(
            namespace, container_params, pod_params, job_params
        )

        # Delete old jobs and pods
        kube_object.delete_old_jobs()
        kube_object.delete_old_pods()

        kube_object.create_namespace()
        kube_object.launch_worker()

    elif args.subcommand == "mcs":

        logging.info("Executing monte carlo simulation for GBM model.")

        container_params = dict(
            name="market-risk-models",
            image_pull_policy="Never",
            image="market-risk-models:latest",
            args=[
                args.model_name,
                args.num_simulations,
                args.starting_value,
                args.mu,
                args.sigma,
                args.forecast_period,
                args.num_trading_days,
            ],
        )

        pod_params = dict(
            name=f"mrm-{uuid.uuid4()}",
            restart_policy="Never",
            labels=dict(name="market-risk-models", type="pod"),
        )

        job_params = dict(
            name=f"mrm-{uuid.uuid4()}",
            labels=dict(name="market-risk-models", type="job"),
        )

        kube_object = ModelOrchestrator(
            namespace, container_params, pod_params, job_params
        )

        # Delete old jobs and pods
        kube_object.delete_old_jobs()
        kube_object.delete_old_pods()

        kube_object.create_namespace()
        kube_object.launch_worker()

    else:

        logging.info(f"Unknown model {args.subcommand}")
