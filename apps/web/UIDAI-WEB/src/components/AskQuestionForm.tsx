export default function AskQuestionForm() {
  return (
    <div className="ask-section">
      <h3 className="section-title">Ask a Question</h3>

      <form className="ask-form">
        <div className="form-group">
          <label>Full Name</label>
          <input type="text" placeholder="Enter your name" />
        </div>

        <div className="form-group">
          <label>Email Address</label>
          <input type="email" placeholder="Enter your email" />
        </div>

        <div className="form-group">
          <label>Category</label>
          <select>
            <option>General</option>
            <option>Enrolment</option>
            <option>Demographic Update</option>
            <option>Biometric Update</option>
          </select>
        </div>

        <div className="form-group">
          <label>Question</label>
          <textarea
            rows={4}
            placeholder="Enter your question here"
          />
        </div>

        <button type="submit" className="submit-btn">
          Submit Query
        </button>
      </form>
    </div>
  );
}
