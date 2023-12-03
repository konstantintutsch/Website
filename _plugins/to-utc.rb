module Jekyll
  module TOUTC
    def utc(stamp)
      time(stamp).utc
    end
  end
end

Liquid::Template.register_filter(Jekyll::TOUTC)
