export function comprehensionFailure(failureCount) {
  if (!Number.isInteger(failureCount) || failureCount < 0) throw new Error('FAILURE_COUNT');
  const next = failureCount + 1;
  return next === 1
    ? {failureCount:1,result:'RETRY',calibrationAllowed:false}
    : {failureCount:next,result:'FAIL',calibrationAllowed:false};
}

export function comprehensionPass(failureCount=0) {
  if (!Number.isInteger(failureCount) || failureCount < 0) throw new Error('FAILURE_COUNT');
  return {failureCount,result:'PASS',calibrationAllowed:true};
}

export function assertCalibrationAllowed(comprehensionPassed) {
  if (comprehensionPassed !== true) throw new Error('CALIBRATION_BEFORE_COMPREHENSION');
  return true;
}

export function nextAfterAttempt(index) {
  if (!Number.isInteger(index) || index < 0 || index > 11) throw new Error('ATTEMPT_INDEX');
  if (index === 5) return {kind:'BREAK',nextIndex:6};
  if (index === 11) return {kind:'COMPLETE',nextIndex:12};
  return {kind:'NEXT',nextIndex:index+1};
}
