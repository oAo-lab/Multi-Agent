interface WorkflowStepsProps {
  currentStep: number;
}

const steps = ['流程创建', 'Agent分配', '任务执行', '结果汇总'];

export default function WorkflowSteps({ currentStep }: WorkflowStepsProps) {
  return (
    <ul className="steps steps-vertical lg:steps-horizontal mb-12">
      {steps.map((step, index) => (
        <li 
          key={step}
          className={`step ${index <= currentStep ? 'step-primary' : ''}`}
        >
          {step}
        </li>
      ))}
    </ul>
  );
}
