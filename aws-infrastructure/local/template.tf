provider "aws" {

  region                      = "us-east-1"
  access_key                  = "localstack"
  secret_key                  = "localstack"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  s3_force_path_style         = true
  skip_requesting_account_id  = true

  endpoints{
    sqs = "http://localhost:31000"
    s3 = "http://localhost:31002"

    /*apigateway     = "http://localhost:4567"
    cloudformation = "http://localhost:4581"
    cloudwatch     = "http://localhost:4582"
    dynamodb       = "http://localhost:4569"
    es             = "http://localhost:4578"
    firehose       = "http://localhost:4573"
    iam            = "http://localhost:4593"
    kinesis        = "http://localhost:4568"
    kms            = "http://localhost:4599"
    lambda         = "http://localhost:4574"
    route53        = "http://localhost:4580"
    redshift       = "http://localhost:4577"
    s3             = "http://localhost:4572"
    secretsmanager = "http://localhost:4584"
    ses            = "http://localhost:4579"
    sns            = "http://localhost:4575"
    sqs            = "http://localhost:4576"
    ssm            = "http://localhost:4583"
    stepfunctions  = "http://localhost:4585"
    sts            = "http://localhost:4592"*/
  }

}

/* SQS Message Queue with Policy */
resource "aws_sqs_queue" "sqs_queue_ingest" {
  name = "data-ingestion-queue"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:*:*:data-ingestion-queue",
      "Condition": {
        "ArnLike": { "aws:SourceArn": "${aws_s3_bucket.s3_bucket_ingest_kmv.arn}"}
      }
    }
  ]
}
POLICY
}


/* S3 Ingest Buckets */
resource "aws_s3_bucket" "s3_bucket_ingest_kmv"{
   bucket = "kubeq-ingest-kmv"
   acl    = "private"
   tags = {
      Name = "Ingest-KMV-Bucket"
    }

  }

/* S3 Output Buckets */
resource "aws_s3_bucket" "s3_bucket_output_kmv"{
   bucket = "kubeq-output-kmv"
   acl    = "private"
   tags = {
      Name = "Output-KMV-Bucket"
    }

  }


/* Notifications */
resource "aws_s3_bucket_notification" "bucket_notification_kmv" {
  bucket = aws_s3_bucket.s3_bucket_ingest_kmv.id

  queue {
    queue_arn     = aws_sqs_queue.sqs_queue_ingest.arn
    events        = ["s3:ObjectCreated:*"]
  }
}