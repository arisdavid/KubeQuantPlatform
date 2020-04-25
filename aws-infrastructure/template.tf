
provider "aws" {

  region = "us-east-1"
  
}

/* SQS Message Queue with Policy */
resource "aws_sqs_queue" "sqs_queue_ingest" {
  name = "s3-event-notification-queue"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:*:*:s3-event-notification-queue",
      "Condition": {
        "ArnLike": { "aws:SourceArn": "${aws_s3_bucket.s3_bucket_ingest_gbm.arn}"}
      }
    }
  ]
}
POLICY
}


/* S3 Buckets */
resource "aws_s3_bucket" "s3_bucket_ingest_gbm"{
   bucket = "rqmp-ingest-gbm"
   acl    = "private"
   tags = {
      Name = "Ingest-GBM-Bucket"
    }

  }

  resource "aws_s3_bucket" "s3_bucket_ingest_kmv"{
   bucket = "rqmp-ingest-kmv"
   acl    = "private"

   tags = {
      Name = "Ingest-KMV-Bucket"
    }
}


/* Notifications */
resource "aws_s3_bucket_notification" "bucket_notification_gbm" {
  bucket = aws_s3_bucket.s3_bucket_ingest_gbm.id

  queue {
    queue_arn     = aws_sqs_queue.sqs_queue_ingest.arn
    events        = ["s3:ObjectCreated:*"]
  }
}
