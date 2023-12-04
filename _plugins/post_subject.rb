Jekyll::Hooks.register :posts, :pre_render do |post|
  post.data['subject'] = "?subject=Post: " + post.data['title']
end
