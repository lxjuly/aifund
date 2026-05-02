#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { TradingAgentsGpuHostStack } from "../lib/tradingagents-gpu-host-stack";

const app = new cdk.App();

new TradingAgentsGpuHostStack(app, "TradingAgentsGpuHostStack", {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
  description: "Single-host GPU inference stack for TradingAgents.",
});
