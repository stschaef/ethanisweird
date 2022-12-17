import React from 'react';
import PropTypes from 'prop-types';

class Comments extends React.Component {
  /* Display comments for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { comments_arr: [] , new_comment : ""};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    // Call REST API to get list of comments
    fetch(this.props.url, { credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then((data) => {
      this.setState({
        comments_arr: data.comments
      });
    })
    .catch(error => console.log(error));  // eslint-disable-line no-console
  }

  handleSubmit(event) {
    event.preventDefault();
    // console.log("Enter");
    // console.log(this.state.new_comment);
    fetch(this.props.url, {
      method: 'POST',
      body: JSON.stringify(this.state.new_comment),
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      }
    }).then(response => {
      if (response.status >= 200 && response.status < 300) {
          this.componentDidMount();
          this.setState({new_comment : ""});
          return response;
          console.log(response);
        } else {
         console.log('Somthing happened wrong');
        }
  }).catch(err => err);
  }

  handleChange(event) {
    // console.log(event.target.value);
    this.setState({
      new_comment : event.target.value
    });
  }
  

  render() {
    const listItems = this.state.comments_arr.map((comment, i) => {
      return (
        <li key={i}><a href={comment.owner_show_url}><p>
          {comment.owner} 
        </p></a><p> {comment.text} </p></li>
      )});

    // Render list of comments
    return (
      <div className="comments">
      <ul>
        {listItems}
      </ul>
      <form onSubmit={this.handleSubmit} onChange={this.handleChange} id="comment-form">
        <input type="text" value={this.state.new_comment} />
      </form>
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;
