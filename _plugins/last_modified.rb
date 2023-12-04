def apply_modified(page)
  unless page.data['title'] == "Blog" || page.data['title'] == "Archive"
    # get last modified from file system
    modification_time = File.mtime page.path
  end

  # insert into page.last-modified
  page.data['last_modified'] = modification_time
end

Jekyll::Hooks.register :pages, :pre_render do |page|
  apply_modified page
end
Jekyll::Hooks.register :posts, :pre_render do |post|
  apply_modified post
end
