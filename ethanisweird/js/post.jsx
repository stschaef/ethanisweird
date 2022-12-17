import React from 'react';
import PropTypes from 'prop-types';
import Comments from './comments';
import Likes from './likes';

// TO DO: Will want to call likes and comments somewhere in this file

class Post extends React.Component {
  /* Display one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  /*Example:
  {
      "age": "2017-09-28 04:33:28",
      "img_url": "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg",
      "owner": "awdeorio",
      "owner_img_url": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "owner_show_url": "/u/awdeorio/",
      "post_show_url": "/p/3/",
      "url": "/api/v1/p/3/"
  }*/

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
        age: Date.now(),
        img_url: "",
        owner: "",
        owner_img_url: "",
        owner_show_url: "",
        post_show_url: ""
    };
  }

  componentDidMount() {
    // Call REST API to get number of likes
    fetch(this.props.url, { credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then((data) => {
      this.setState({
        age: data.age,
        img_url: data.img_url,
        owner: data.owner,
        owner_img_url: data.owner_img_url,
        owner_show_url: data.owner_show_url,
        post_show_url: data.post_show_url,
      });
    })
    .catch(error => console.log(error));  // eslint-disable-line no-console
  }

  render() {
      const owner_img = <img src={this.state.owner_img_url} alt="Owner image" style={{width: '100px'}}/>;
      const owner_info = <a href={this.state.owner_show_url}><p>
                        {this.state.owner}
                        </p></a>;
      const image = <a href={this.state.post_show_url}>
                    <img src={this.state.img_url} alt="Posted image" style={{width: '400px'}}/>
                    </a>;
      const comments_source = this.props.url + "comments/";
      const likes_source = this.props.url + "likes/";

      return (
          <div className="post" style = {{border: 'solid'}}>
            {owner_img}
            {owner_info}
            {image}
            <div className="likes">
            <Likes url={likes_source} />
            </div>
            <div className="comments">
            <Comments  url={comments_source} />
            </div>
          </div>
      );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
