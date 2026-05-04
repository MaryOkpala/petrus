variable "team" {
  type = string
}

variable "environment" {
  type = string
}

variable "environment_type" {
  type    = string
  default = "web-app"
}

variable "cpu_request_limit" {
  type    = string
  default = "4"
}

variable "memory_request_limit" {
  type    = string
  default = "8Gi"
}

variable "cpu_limit" {
  type    = string
  default = "8"
}

variable "memory_limit" {
  type    = string
  default = "16Gi"
}

variable "pod_limit" {
  type    = string
  default = "20"
}
