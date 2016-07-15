class Geeknote < Formula
  desc "Command-line client for Evernote"
  homepage 'http://www.geeknote.me/'
  head 'https://github.com/jeffkowalski/geeknote.git'

  depends_on :python

  resource "oauth2" do
    url "https://pypi.python.org/packages/source/o/oauth2/oauth2-1.9.0.post1.tar.gz"
    sha256 "c006a85e7c60107c7cc6da1b184b5c719f6dd7202098196dfa6e55df669b59bf"
  end

  resource "httplib2" do
    url "https://pypi.python.org/packages/source/h/httplib2/httplib2-0.9.2.tar.gz"
    sha256 "c3aba1c9539711551f4d83e857b316b5134a1c4ddce98a875b7027be7dd6d988"
  end

  resource "evernote" do
    url "https://pypi.python.org/packages/source/e/evernote/evernote-1.25.1.tar.gz"
    sha256 "6f9838307e28819954c18b92eed5616b91aa4b2230c2ee325f44d97cde9d12a8"
  end

  resource "html2text" do
    url "https://pypi.python.org/packages/source/h/html2text/html2text-2016.1.8.tar.gz"
    sha256 "088046f9b126761ff7e3380064d4792279766abaa5722d0dd765d011cf0bb079"
  end

  resource "SQLAlchemy" do
    url "https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-1.0.12.tar.gz"
    sha256 "6679e20eae780b67ba136a4a76f83bb264debaac2542beefe02069d0206518d1"
  end

  resource "markdown2" do
    url "https://pypi.python.org/packages/source/m/markdown2/markdown2-2.3.0.zip"
    sha256 "c8e29ba47a0e408bb92df75d5c6361c84268c54c5320d53ffd4961c546f77f1c"
  end

  resource "beautifulsoup4" do
    url "https://pypi.python.org/packages/source/b/beautifulsoup4/beautifulsoup4-4.4.1.tar.gz"
    sha256 "87d4013d0625d4789a4f56b8d79a04d5ce6db1152bb65f1d39744f7709a366b4"
  end

  resource "thrift" do
    url "https://pypi.python.org/packages/source/t/thrift/thrift-0.9.3.tar.gz"
    sha256 "dfbc3d3bd19d396718dab05abaf46d93ae8005e2df798ef02e32793cd963877e"
  end

  resource "proxyenv" do
    url "https://pypi.python.org/packages/69/98/46baccf9ce353828726e0d302dad201e634fe4b50f6f61891f0721f40789/proxyenv-0.5.1.tar.gz"
    sha256 "e73caf8b063b7fbfb93b67e725a71469768262a9dddb4d9dfb79bb1e84cab4b9"
  end

  resource "htpasswd" do
    url "https://pypi.python.org/packages/b9/2f/8b76f8b77125b75c3532966f3291f9e8787268be65fc4c9694887cba9375/htpasswd-2.3.tar.gz"
    sha256 "565f0b647a32549c663ccfddd1f501891daaf29242bbc6174bdd448120383e3d"
  end

  def install
    ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python2.7/site-packages"
    resources.each do |r|
      r.stage do
        system "python", *Language::Python.setup_install_args(libexec/"vendor")
      end
    end

    ENV.prepend_create_path "PYTHONPATH", libexec/"lib/python2.7/site-packages"
    system "python", *Language::Python.setup_install_args(prefix)

    bash_completion.install "completion/bash_completion/_geeknote" => "geeknote"
    zsh_completion.install "completion/zsh_completion/_geeknote" => "_geeknote"

    bin.env_script_all_files(libexec/"bin", :PYTHONPATH => ENV["PYTHONPATH"])
  end

  test do
    system "py.test"
  end
end
