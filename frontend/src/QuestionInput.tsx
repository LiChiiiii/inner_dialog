import { ChangeEvent, FormEvent, useState } from "react";
import { Panel } from "reactflow";
import useStore from "./store";

type FormData = {
  question: string;
  model: string;
};

function QuestionInput() {
  const [formData, setFormData] = useState<FormData>({
    question: "",
    model: "inner_dialog",
  });
  const get_mind_map = useStore((state) => state.getMindMap);
  const layout = useStore((state) => state.layout);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await get_mind_map(formData.question, formData.model);
  };
  const handleTextInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleRadioChange = (event: ChangeEvent<HTMLInputElement>) => {
    setFormData((prevFormData) => ({
      ...prevFormData,
      ["model"]: event.target.value,
    }));
  };

  return (
    <Panel position="top-right">
      <form onSubmit={handleSubmit}>
        <label
          htmlFor="default-search"
          className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
        >
          Question
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <svg
              className="w-4 h-4 text-gray-500 dark:text-gray-400"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 20"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
              />
            </svg>
          </div>
          <input
            value={formData.question}
            type="text"
            id="default-search"
            placeholder="Ask open-ended questions..."
            name="question"
            onChange={handleTextInputChange}
            required
            className="question-text-input"
          />
        </div>
        <button type="submit" className="submit-button">
          Submit
        </button>
      </form>

      <div className="model-select-container">
        <input
          id="bordered-radio-1"
          type="radio"
          value="inner_dialog"
          checked={formData.model === "inner_dialog"}
          onChange={handleRadioChange}
          name="bordered-radio"
          className="radio-input"
        />
        <label htmlFor="bordered-radio-1" className="radio-label">
          Inner Dialog
        </label>
      </div>
      <div className="model-select-container">
        <input
          id="bordered-radio-2"
          type="radio"
          value="palm"
          checked={formData.model === "palm"}
          onChange={handleRadioChange}
          name="bordered-radio"
          className="radio-input"
        />
        <label htmlFor="bordered-radio-2" className="radio-label">
          PALM
        </label>
      </div>
      <div className="model-select-container">
        <input
          id="bordered-radio-2"
          type="radio"
          value="chatgpt"
          checked={formData.model === "chatgpt"}
          onChange={handleRadioChange}
          name="bordered-radio"
          className="radio-input"
        />
        <label htmlFor="bordered-radio-2" className="radio-label">
          ChatGPT
        </label>
      </div>
      <div className="model-select-container">
        <input
          id="bordered-radio-3"
          type="radio"
          value="extract"
          checked={formData.model === "extract"}
          onChange={handleRadioChange}
          name="bordered-radio"
          className="radio-input"
        />
        <label htmlFor="bordered-radio-3" className="radio-label">
          Human
        </label>
      </div>
      <button onClick={() => layout("LR")}>layout</button>
    </Panel>
  );
}
export default QuestionInput;
