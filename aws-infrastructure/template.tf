provider "aws" {

  region = "us-east-1"

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