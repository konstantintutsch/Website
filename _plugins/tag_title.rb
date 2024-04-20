Jekyll::Hooks.register :tags, :pre_render do |tag|
  tag.data['title'] = "Tag: " + tag.data['name']
end
