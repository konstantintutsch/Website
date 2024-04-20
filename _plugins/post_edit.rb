Jekyll::Hooks.register :posts, :pre_render do |post|
  post.data['edit'] = "/website/edit/main/" + post.relative_path
end
